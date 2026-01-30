"""
Wrapper Appwrite pour remplacer Django ORM
Tous les appels de BD passent par l'API Appwrite
"""

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

class AppwriteDB:
    """Wrapper pour tous les accès BD via Appwrite"""
    
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint(settings.APPWRITE_ENDPOINT)
        self.client.set_project(settings.APPWRITE_PROJECT_ID)
        self.client.set_key(settings.APPWRITE_API_KEY)
        
        self.databases = Databases(self.client)
        self.database_id = settings.APPWRITE_DATABASE_ID
        
    def test_connection(self):
        """Tester la connexion Appwrite"""
        try:
            db = self.databases.get(database_id=self.database_id)
            logger.info(f"✅ Appwrite connecté: {db['name']}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur Appwrite: {e}")
            return False
    
    def create_collection(self, collection_id, name, attributes):
        """Créer une collection"""
        try:
            collection = self.databases.create_collection(
                database_id=self.database_id,
                collection_id=collection_id,
                name=name
            )
            
            # Ajouter les attributs
            for attr in attributes:
                # Determine the correct attribute type method
                attr_type = attr.get('type', 'string')
                method_name = f'create_{attr_type}_attribute'
                
                if hasattr(self.databases, method_name):
                    method = getattr(self.databases, method_name)
                    method(
                        database_id=self.database_id,
                        collection_id=collection_id,
                        **attr
                    )
                else:
                    # Fallback to string attribute
                    self.databases.create_string_attribute(
                        database_id=self.database_id,
                        collection_id=collection_id,
                        **attr
                    )
            
            logger.info(f"✅ Collection créée: {collection_id}")
            return collection
        except Exception as e:
            logger.warning(f"Collection {collection_id} existe déjà ou erreur: {e}")
            return None
    
    def create_document(self, collection_id, data, document_id=None):
        """Créer un document"""
        try:
            doc = self.databases.create_document(
                database_id=self.database_id,
                collection_id=collection_id,
                document_id=document_id or 'unique()',
                data=data
            )
            logger.info(f"✅ Document créé: {doc['$id']}")
            return doc
        except Exception as e:
            logger.error(f"❌ Erreur création document: {e}")
            raise
    
    def get_document(self, collection_id, document_id):
        """Récupérer un document"""
        try:
            doc = self.databases.get_document(
                database_id=self.database_id,
                collection_id=collection_id,
                document_id=document_id
            )
            return doc
        except Exception as e:
            logger.error(f"❌ Erreur lecture document: {e}")
            return None
    
    def list_documents(self, collection_id, queries=None):
        """Lister les documents avec filtres optionnels"""
        try:
            result = self.databases.list_documents(
                database_id=self.database_id,
                collection_id=collection_id,
                queries=queries or []
            )
            return result.get('documents', [])
        except Exception as e:
            logger.error(f"❌ Erreur liste documents: {e}")
            return []
    
    def update_document(self, collection_id, document_id, data):
        """Mettre à jour un document"""
        try:
            doc = self.databases.update_document(
                database_id=self.database_id,
                collection_id=collection_id,
                document_id=document_id,
                data=data
            )
            logger.info(f"✅ Document mis à jour: {document_id}")
            return doc
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour: {e}")
            raise
    
    def delete_document(self, collection_id, document_id):
        """Supprimer un document"""
        try:
            self.databases.delete_document(
                database_id=self.database_id,
                collection_id=collection_id,
                document_id=document_id
            )
            logger.info(f"✅ Document supprimé: {document_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur suppression: {e}")
            return False

# Instance globale
_appwrite_db = None

def get_appwrite_db():
    """Singleton pattern - retourner l'instance Appwrite"""
    global _appwrite_db
    if _appwrite_db is None:
        _appwrite_db = AppwriteDB()
    return _appwrite_db
