# Services pour la gestion des fichiers (version MongoDB avec fallback)
from datetime import datetime
import os
import hashlib
import json
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path

class SimpleFileManager:
    """Gestionnaire de fichiers simple pour le développement"""
    
    def __init__(self):
        # Configuration MongoDB
        try:
            from pymongo import MongoClient
            self.client = MongoClient(
                host=getattr(settings, 'MONGO_DB_HOST', 'localhost'),
                port=getattr(settings, 'MONGO_DB_PORT', 27017),
                username=getattr(settings, 'MONGO_DB_USER', None),
                password=getattr(settings, 'MONGO_DB_PASSWORD', None)
            )
            self.mongo_available = True
        except ImportError:
            self.client = None
            self.mongo_available = False
        
        if self.client:
            self.db = self.client[getattr(settings, 'MONGO_DB_NAME', 'enise_filesystem')]
            self.metadata_collection = self.db['file_metadata']
            self.logs_collection = self.db['file_access_logs']
        else:
            self.db = None
            self.metadata_collection = None
            self.logs_collection = None
        
        # Fallback sur système de fichiers local si MongoDB pas disponible
        self.use_mongodb = self.mongo_available and self._test_mongodb_connection()
        if not self.use_mongodb:
            print("⚠️ MongoDB non disponible, utilisation du système de fichiers local")
            self.storage_dir = Path(settings.MEDIA_ROOT) / 'uploads'
            self.metadata_file = self.storage_dir / 'metadata.json'
            self.logs_file = self.storage_dir / 'access_logs.json'
            
            # Créer les dossiers
            self.storage_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialiser les fichiers de métadonnées
            self._init_metadata()
        else:
            print("✅ Connexion MongoDB établie avec succès")
            # Créer les indexes si nécessaire
            self._create_mongodb_indexes()
    
    def _test_mongodb_connection(self):
        """Tester la connexion MongoDB avec timeout court"""
        if not self.client:
            return False
        try:
            # Timeout court (2 secondes max) pour ne pas bloquer le démarrage
            self.client.admin.command('ping', maxTimeMS=2000)
            return True
        except Exception as e:
            print(f"Erreur de connexion MongoDB: {e}")
            return False
    
    def _create_mongodb_indexes(self):
        """Créer les indexes MongoDB pour optimiser les performances"""
        if not self.metadata_collection:
            return
        try:
            # Index sur file_hash pour éviter les doublons
            self.metadata_collection.create_index("file_hash", unique=True)
            # Index sur owner_id pour les requêtes utilisateur
            self.metadata_collection.create_index("owner_id")
            # Index sur category pour les filtres
            self.metadata_collection.create_index("category")
            # Index sur created_at pour le tri
            self.metadata_collection.create_index("created_at")
            # Index composé pour les permissions
            self.metadata_collection.create_index([("owner_id", 1), ("is_public", 1)])
            print("✅ Index MongoDB créés avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de la création des indexes: {e}")
    
    def _init_metadata(self):
        """Initialiser les fichiers de métadonnées (mode fallback)"""
        if self.use_mongodb:
            return  # Pas besoin si MongoDB est disponible
            
        if not self.metadata_file.exists():
            with open(self.metadata_file, 'w') as f:
                json.dump([], f)
        
        if not self.logs_file.exists():
            with open(self.logs_file, 'w') as f:
                json.dump([], f)
    
    def _load_metadata(self):
        """Charger les métadonnées"""
        if self.use_mongodb and self.metadata_collection:
            try:
                return list(self.metadata_collection.find())
            except:
                return []
        else:
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return []
    
    def _save_metadata(self, metadata):
        """Sauvegarder les métadonnées"""
        # Cette méthode n'est pas utilisée en mode MongoDB
        if not self.use_mongodb:
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
    
    def _log_access(self, file_id, user_id, access_type, success=True):
        """Logger un accès"""
        log_entry = {
            'file_id': file_id,
            'user_id': user_id,
            'access_type': access_type,
            'timestamp': datetime.now(),
            'success': success
        }
        
        if self.use_mongodb and hasattr(self, 'logs_collection') and self.logs_collection:
            self.logs_collection.insert_one(log_entry)
        else:
            logs = self._load_logs()
            logs.append(log_entry)
            with open(self.logs_file, 'w') as f:
                json.dump(logs, f, indent=2, default=str)
    
    def _load_logs(self):
        """Charger les logs"""
        try:
            with open(self.logs_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def upload_file(self, file_data, filename, user_id, is_public=False, tags=None):
        """Uploader un fichier"""
        try:
            # Calculer le hash du fichier
            file_hash = self._calculate_file_hash(file_data)
            
            # Vérifier si le fichier existe déjà
            if self.use_mongodb:
                existing = self.metadata_collection.find_one({'file_hash': file_hash})
            else:
                metadata = self._load_metadata()
                existing = next((file_meta for file_meta in metadata if file_meta.get('file_hash') == file_hash), None)
            
            if existing:
                return {'success': False, 'message': 'File already exists', 'file_id': existing.get('id')}
            
            # Générer un ID unique
            file_id = f"file_{int(datetime.now().timestamp() * 1000)}"
            
            # Créer les métadonnées
            file_meta = {
                'id': file_id,
                'filename': filename,
                'original_filename': filename,
                'file_size': file_data.size,
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
            
            if self.use_mongodb:
                # Stocker en utilisant GridFS
                try:
                    from gridfs import GridFS
                    fs = GridFS(self.db)
                    fs.put(file_data.read(), filename=filename, metadata=file_meta)
                    self.metadata_collection.insert_one(file_meta)
                except ImportError:
                    # Fallback: stocker les métadonnées seulement
                    file_meta['file_data'] = file_data.read()
                    self.metadata_collection.insert_one(file_meta)
            else:
                # Stocker sur système de fichiers local
                file_path = self.storage_dir / filename
                with open(file_path, 'wb+') as destination:
                    for chunk in file_data.chunks():
                        destination.write(chunk)
                file_meta['file_path'] = str(file_path)
                
                metadata = self._load_metadata()
                metadata.append(file_meta)
                self._save_metadata(metadata)
            
            # Logger l'upload
            self._log_access(file_id, user_id, 'upload')
            
            return {
                'success': True,
                'file_id': file_id,
                'message': 'File uploaded successfully'
            }
            
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_file(self, file_id, user_id=None):
        """Récupérer un fichier"""
        try:
            metadata = self._load_metadata()
            
            # Trouver le fichier
            file_meta = None
            for meta in metadata:
                if meta.get('id') == file_id:
                    file_meta = meta
                    break
            
            if not file_meta:
                return None
            
            # Vérifier l'accès
            if not self._check_permission(file_meta, user_id):
                return None
            
            # Logger l'accès
            self._log_access(file_id, user_id, 'view')
            
            # Mettre à jour les statistiques
            file_meta['view_count'] = file_meta.get('view_count', 0) + 1
            file_meta['updated_at'] = datetime.now().isoformat()
            self._save_metadata(metadata)
            
            # Lire le fichier
            with open(file_meta['file_path'], 'rb') as f:
                file_data = f.read()
            
            return file_data, file_meta
            
        except Exception:
            return None
    
    def list_files(self, user_id, category=None, tags=None):
        """Lister les fichiers"""
        try:
            metadata = self._load_metadata()
            
            # Filtrer par permissions
            filtered_files = []
            for file_meta in metadata:
                if self._check_permission(file_meta, user_id):
                    if not category or file_meta.get('category') == category:
                        if not tags or any(tag in file_meta.get('tags', []) for tag in tags):
                            filtered_files.append(file_meta)
            
            # Trier par date de création
            filtered_files.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            return filtered_files
            
        except Exception:
            return []
    
    def delete_file(self, file_id, user_id, is_admin=False):
        """Supprimer un fichier"""
        try:
            metadata = self._load_metadata()
            
            # Trouver le fichier
            file_meta = None
            for i, meta in enumerate(metadata):
                if meta.get('id') == file_id:
                    file_meta = meta
                    break
            
            if not file_meta:
                return False
            
            # Vérifier les permissions
            if not is_admin and file_meta.get('owner_id') != user_id:
                return False
            
            # Supprimer le fichier physique
            file_path = Path(file_meta['file_path'])
            if file_path.exists():
                file_path.unlink()
            
            # Supprimer les métadonnées
            metadata = [meta for meta in metadata if meta.get('id') != file_id]
            self._save_metadata(metadata)
            
            # Logger la suppression
            self._log_access(file_id, user_id, 'delete')
            
            return True
            
        except Exception:
            return False
    
    def get_access_logs(self, file_id=None, user_id=None):
        """Récupérer les logs d'accès"""
        try:
            logs = self._load_logs()
            
            # Filtrer
            filtered_logs = []
            for log in logs:
                if (not file_id or log.get('file_id') == file_id) and \
                   (not user_id or log.get('user_id') == user_id):
                    filtered_logs.append(log)
            
            # Trier par date
            filtered_logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return filtered_logs
            
        except Exception:
            return []
    
    # Méthodes utilitaires
    def _calculate_file_hash(self, file_data):
        """Calculer le hash SHA256"""
        hash_sha256 = hashlib.sha256()
        for chunk in file_data.chunks():
            hash_sha256.update(chunk)
        file_data.seek(0)  # Remettre le curseur au début
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
    
    def _check_permission(self, file_meta, user_id):
        """Vérifier si un utilisateur a accès à un fichier"""
        if file_meta.get('is_public'):
            return True
        if file_meta.get('owner_id') == user_id:
            return True
        if user_id in file_meta.get('allowed_users', []):
            return True
        return False

# Instance globale (lazy initialization)
_file_manager = None

def get_file_manager():
    """Get or create the file manager instance (lazy initialization)"""
    global _file_manager
    if _file_manager is None:
        _file_manager = SimpleFileManager()
    return _file_manager

# Backward compatibility
class FileManagerProxy:
    """Proxy pour backward compatibility"""
    def __getattr__(self, name):
        return getattr(get_file_manager(), name)

file_manager = FileManagerProxy()