# Services pour la gestion des fichiers et des accès avec MongoDB
from datetime import datetime
from pymongo import MongoClient
from gridfs import GridFS
import hashlib
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class MongoDBFileManager:
    """Gestionnaire de fichiers MongoDB avec GridFS"""
    
    def __init__(self):
        # Connexion à MongoDB
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['enise_filesystem']
        self.fs = GridFS(self.db)
        
        # Collections pour les métadonnées
        self.metadata_collection = self.db['file_metadata']
        self.access_logs = self.db['file_access_logs']
        self.permissions = self.db['user_permissions']
    
    def upload_file(self, file_data, filename, user_id, is_public=False, tags=None):
        """Uploader un fichier dans GridFS MongoDB"""
        try:
            # Calculer le hash du fichier
            file_hash = self._calculate_file_hash(file_data)
            
            # Vérifier si le fichier existe déjà
            existing_file = self.metadata_collection.find_one({'file_hash': file_hash})
            if existing_file:
                return {'success': False, 'message': 'File already exists', 'file_id': str(existing_file['_id'])}
            
            # Stocker le fichier dans GridFS
            file_id = self.fs.put(file_data, filename=filename)
            
            # Créer les métadonnées
            metadata = {
                'filename': filename,
                'original_filename': filename,
                'file_size': len(file_data) if isinstance(file_data, bytes) else file_data.size,
                'file_hash': file_hash,
                'mime_type': self._get_mime_type(filename),
                'category': self._get_file_category(filename),
                'tags': tags or [],
                'owner_id': user_id,
                'is_public': is_public,
                'allowed_users': [],
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'download_count': 0,
                'view_count': 0
            }
            
            # Insérer les métadonnées
            result = self.metadata_collection.insert_one(metadata)
            
            # Logger l'upload
            self._log_access(str(result.inserted_id), user_id, 'upload')
            
            return {
                'success': True,
                'file_id': str(result.inserted_id),
                'message': 'File uploaded successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_file(self, file_id, user_id=None):
        """Récupérer un fichier depuis GridFS"""
        try:
            # Vérifier les permissions
            metadata = self.metadata_collection.find_one({'_id': file_id})
            if not metadata:
                return None
            
            # Vérifier l'accès
            if not self._check_permission(metadata, user_id):
                return None
            
            # Logger l'accès
            self._log_access(file_id, user_id, 'view')
            
            # Récupérer le fichier
            file_data = self.fs.get(file_id)
            
            # Mettre à jour les statistiques
            self.metadata_collection.update_one(
                {'_id': file_id},
                {'$inc': {'view_count': 1}, '$set': {'last_accessed': datetime.now()}}
            )
            
            return file_data, metadata
            
        except Exception:
            return None
    
    def list_files(self, user_id, category=None, tags=None):
        """Lister les fichiers accessibles à un utilisateur"""
        try:
            query = {
                '$or': [
                    {'is_public': True},
                    {'owner_id': user_id},
                    {'allowed_users': user_id}
                ]
            }
            
            if category:
                query['category'] = category
            
            if tags:
                query['tags'] = {'$in': tags}
            
            files = self.metadata_collection.find(query).sort('created_at', -1)
            
            return list(files)
            
        except Exception:
            return []
    
    def delete_file(self, file_id, user_id, is_admin=False):
        """Supprimer un fichier"""
        try:
            metadata = self.metadata_collection.find_one({'_id': file_id})
            if not metadata:
                return False
            
            # Vérifier les permissions
            if not is_admin and metadata['owner_id'] != user_id:
                return False
            
            # Supprimer de GridFS
            self.fs.delete(file_id)
            
            # Supprimer les métadonnées
            self.metadata_collection.delete_one({'_id': file_id})
            
            # Logger la suppression
            self._log_access(file_id, user_id, 'delete')
            
            return True
            
        except Exception:
            return False
    
    def grant_access(self, file_id, user_ids):
        """Donner l'accès à un fichier à des utilisateurs spécifiques"""
        try:
            self.metadata_collection.update_one(
                {'_id': file_id},
                {'$addToSet': {'allowed_users': {'$each': user_ids}}}
            )
            return True
        except Exception:
            return False
    
    def revoke_access(self, file_id, user_ids):
        """Révoquer l'accès à un fichier"""
        try:
            self.metadata_collection.update_one(
                {'_id': file_id},
                {'$pull': {'allowed_users': {'$in': user_ids}}}
            )
            return True
        except Exception:
            return False
    
    def get_access_logs(self, file_id=None, user_id=None):
        """Récupérer les logs d'accès"""
        query = {}
        if file_id:
            query['file_id'] = file_id
        if user_id:
            query['user_id'] = user_id
        
        return list(self.access_logs.find(query).sort('timestamp', -1))
    
    # Méthodes utilitaires
    def _calculate_file_hash(self, file_data):
        """Calculer le hash SHA256"""
        hash_sha256 = hashlib.sha256()
        if isinstance(file_data, bytes):
            hash_sha256.update(file_data)
        else:
            for chunk in file_data.chunks():
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _get_mime_type(self, filename):
        """Déterminer le type MIME"""
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.mp4': 'video/mp4',
            '.mp3': 'audio/mpeg',
            '.zip': 'application/zip'
        }
        return mime_types.get(ext, 'application/octet-stream')
    
    def _get_file_category(self, filename):
        """Déterminer la catégorie du fichier"""
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return 'image'
        elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
            return 'video'
        elif ext in ['.mp3', '.wav', '.flac', '.aac']:
            return 'audio'
        elif ext in ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx']:
            return 'document'
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return 'archive'
        else:
            return 'other'
    
    def _check_permission(self, metadata, user_id):
        """Vérifier si un utilisateur a accès à un fichier"""
        if metadata['is_public']:
            return True
        if metadata['owner_id'] == user_id:
            return True
        if user_id in metadata.get('allowed_users', []):
            return True
        return False
    
    def _log_access(self, file_id, user_id, access_type, success=True):
        """Logger un accès"""
        log_entry = {
            'file_id': file_id,
            'user_id': user_id,
            'access_type': access_type,
            'timestamp': datetime.now(),
            'success': success
        }
        self.access_logs.insert_one(log_entry)