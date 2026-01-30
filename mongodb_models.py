# Models MongoDB pour la gestion des fichiers et des accès
from mongoengine import Document, fields, signals
from datetime import datetime
import hashlib
import os

class FileAccessLog(Document):
    """Journal d'accès aux fichiers"""
    meta = {'collection': 'file_access_logs'}
    
    file_id = fields.ObjectIdField(required=True)
    user_id = fields.StringField(required=True)
    access_type = fields.StringField(choices=['view', 'download', 'upload', 'delete'])
    ip_address = fields.StringField()
    user_agent = fields.StringField()
    timestamp = fields.DateTimeField(default=datetime.now)
    success = fields.BooleanField(default=True)

class FileMetadata(Document):
    """Métadonnées des fichiers stockés"""
    meta = {'collection': 'file_metadata'}
    
    # Informations de base
    filename = fields.StringField(required=True, max_length=255)
    original_filename = fields.StringField(required=True, max_length=255)
    file_path = fields.StringField(required=True)
    file_size = fields.IntField(required=True)
    file_hash = fields.StringField(required=True, unique=True)
    mime_type = fields.StringField()
    
    # Catégorisation
    category = fields.StringField(choices=[
        'document', 'image', 'video', 'audio', 'archive', 'other'
    ])
    tags = fields.ListField(fields.StringField())
    
    # Propriétaire et permissions
    owner_id = fields.StringField(required=True)
    owner_name = fields.StringField()
    is_public = fields.BooleanField(default=False)
    allowed_users = fields.ListField(fields.StringField())  # IDs des utilisateurs autorisés
    
    # Timestamps
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    last_accessed = fields.DateTimeField()
    
    # Statistiques
    download_count = fields.IntField(default=0)
    view_count = fields.IntField(default=0)
    
    def calculate_hash(self):
        """Calculer le hash SHA256 du fichier"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(self.file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return None

class UserPermission(Document):
    """Gestion des permissions utilisateur"""
    meta = {'collection': 'user_permissions'}
    
    user_id = fields.StringField(required=True, unique=True)
    username = fields.StringField(required=True)
    email = fields.EmailField()
    
    # Permissions globales
    is_admin = fields.BooleanField(default=False)
    can_upload = fields.BooleanField(default=True)
    can_download = fields.BooleanField(default=True)
    can_delete_own = fields.BooleanField(default=True)
    can_delete_others = fields.BooleanField(default=False)
    
    # Limites de stockage (en octets)
    storage_limit = fields.IntField(default=1073741824)  # 1GB par défaut
    current_storage_used = fields.IntField(default=0)
    
    # Statuts
    is_active = fields.BooleanField(default=True)
    last_login = fields.DateTimeField()
    created_at = fields.DateTimeField(default=datetime.now)

# Signaux pour la mise à jour automatique
signals.pre_save.connect(lambda sender, document: setattr(document, 'updated_at', datetime.now()), sender=FileMetadata)