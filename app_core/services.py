"""
Service layer for database operations using Appwrite
Replaces Django ORM with Appwrite API calls
"""

from enise_site.appwrite_db import get_appwrite_db
from appwrite.query import Query
from django.utils.text import slugify
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class AppwriteService:
    """Base service class for Appwrite operations"""
    
    def __init__(self):
        self.db = get_appwrite_db()
    
    @staticmethod
    def to_dict(doc):
        """Convert Appwrite document to dict, handling $id and other special fields"""
        if not doc:
            return None
        result = dict(doc)
        # Keep the document ID as 'id' for convenience
        if '$id' in result:
            result['id'] = result['$id']
        return result


class SpecialiteService(AppwriteService):
    """Service for Specialite operations"""
    
    COLLECTION_ID = 'specialites'
    
    def list_all(self):
        """Get all specialites, ordered by ordre then nom"""
        try:
            docs = self.db.list_documents(
                self.COLLECTION_ID,
                queries=[Query.order_asc('ordre'), Query.order_asc('nom')]
            )
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing specialites: {e}")
            return []
    
    def get_by_slug(self, slug):
        """Get a specialite by slug"""
        try:
            docs = self.db.list_documents(
                self.COLLECTION_ID,
                queries=[Query.equal('slug', slug)]
            )
            if docs:
                return self.to_dict(docs[0])
            return None
        except Exception as e:
            logger.error(f"Error getting specialite by slug {slug}: {e}")
            return None
    
    def get_by_id(self, doc_id):
        """Get a specialite by document ID"""
        try:
            doc = self.db.get_document(self.COLLECTION_ID, doc_id)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error getting specialite {doc_id}: {e}")
            return None
    
    def create(self, nom, description, image_url=None, icone=None, ordre=0):
        """Create a new specialite"""
        try:
            slug = slugify(nom)
            doc = self.db.create_document(
                self.COLLECTION_ID,
                {
                    'nom': nom,
                    'slug': slug,
                    'description': description,
                    'image_url': image_url or '',
                    'icone': icone or '',
                    'ordre': ordre,
                }
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error creating specialite: {e}")
            raise
    
    def update(self, doc_id, **kwargs):
        """Update a specialite"""
        try:
            doc = self.db.update_document(self.COLLECTION_ID, doc_id, kwargs)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error updating specialite {doc_id}: {e}")
            raise
    
    def delete(self, doc_id):
        """Delete a specialite"""
        try:
            return self.db.delete_document(self.COLLECTION_ID, doc_id)
        except Exception as e:
            logger.error(f"Error deleting specialite {doc_id}: {e}")
            return False


class ActualiteService(AppwriteService):
    """Service for Actualite operations"""
    
    COLLECTION_ID = 'actualites'
    
    def list_published(self, limit=None):
        """Get published actualites, ordered by date (newest first)"""
        try:
            queries = [
                Query.equal('est_publie', True),
                Query.order_desc('date_publication'),
            ]
            if limit:
                queries.append(Query.limit(limit))
            
            docs = self.db.list_documents(self.COLLECTION_ID, queries=queries)
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing published actualites: {e}")
            return []
    
    def list_all(self):
        """Get all actualites (published and unpublished)"""
        try:
            docs = self.db.list_documents(
                self.COLLECTION_ID,
                queries=[Query.order_desc('date_publication')]
            )
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing all actualites: {e}")
            return []
    
    def get_by_slug(self, slug):
        """Get an actualite by slug"""
        try:
            docs = self.db.list_documents(
                self.COLLECTION_ID,
                queries=[Query.equal('slug', slug)]
            )
            if docs:
                return self.to_dict(docs[0])
            return None
        except Exception as e:
            logger.error(f"Error getting actualite by slug {slug}: {e}")
            return None
    
    def get_by_id(self, doc_id):
        """Get an actualite by document ID"""
        try:
            doc = self.db.get_document(self.COLLECTION_ID, doc_id)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error getting actualite {doc_id}: {e}")
            return None
    
    def create(self, titre, contenu, image_url=None, est_publie=True):
        """Create a new actualite"""
        try:
            slug = slugify(titre)
            doc = self.db.create_document(
                self.COLLECTION_ID,
                {
                    'titre': titre,
                    'slug': slug,
                    'contenu': contenu,
                    'image_url': image_url or '',
                    'date_publication': datetime.now().isoformat(),
                    'est_publie': est_publie,
                }
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error creating actualite: {e}")
            raise
    
    def update(self, doc_id, **kwargs):
        """Update an actualite"""
        try:
            doc = self.db.update_document(self.COLLECTION_ID, doc_id, kwargs)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error updating actualite {doc_id}: {e}")
            raise
    
    def delete(self, doc_id):
        """Delete an actualite"""
        try:
            return self.db.delete_document(self.COLLECTION_ID, doc_id)
        except Exception as e:
            logger.error(f"Error deleting actualite {doc_id}: {e}")
            return False


class ContactService(AppwriteService):
    """Service for Contact operations"""
    
    COLLECTION_ID = 'contact'
    
    def list_all(self, unread_only=False):
        """Get all contact messages, ordered by date (newest first)"""
        try:
            queries = [Query.order_desc('date_envoi')]
            if unread_only:
                queries.append(Query.equal('traite', False))
            
            docs = self.db.list_documents(self.COLLECTION_ID, queries=queries)
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing contact messages: {e}")
            return []
    
    def get_by_id(self, doc_id):
        """Get a contact message by ID"""
        try:
            doc = self.db.get_document(self.COLLECTION_ID, doc_id)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error getting contact {doc_id}: {e}")
            return None
    
    def create(self, nom, email, sujet, message):
        """Create a new contact message"""
        try:
            doc = self.db.create_document(
                self.COLLECTION_ID,
                {
                    'nom': nom,
                    'email': email,
                    'sujet': sujet,
                    'message': message,
                    'date_envoi': datetime.now().isoformat(),
                    'traite': False,
                }
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error creating contact message: {e}")
            raise
    
    def mark_as_treated(self, doc_id):
        """Mark a contact message as treated"""
        try:
            doc = self.db.update_document(
                self.COLLECTION_ID,
                doc_id,
                {'traite': True}
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error marking contact as treated: {e}")
            raise
    
    def delete(self, doc_id):
        """Delete a contact message"""
        try:
            return self.db.delete_document(self.COLLECTION_ID, doc_id)
        except Exception as e:
            logger.error(f"Error deleting contact {doc_id}: {e}")
            return False


class PartenairesService(AppwriteService):
    """Service for Partenaires operations"""
    
    COLLECTION_ID = 'partenaires'
    
    def list_all(self, type_partenaire=None):
        """Get all partenaires, optionally filtered by type"""
        try:
            queries = []
            if type_partenaire:
                queries.append(Query.equal('type_partenaire', type_partenaire))
            
            docs = self.db.list_documents(self.COLLECTION_ID, queries=queries)
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing partenaires: {e}")
            return []
    
    def get_by_id(self, doc_id):
        """Get a partenaire by ID"""
        try:
            doc = self.db.get_document(self.COLLECTION_ID, doc_id)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error getting partenaire {doc_id}: {e}")
            return None
    
    def create(self, nom, logo_url, type_partenaire, url=None):
        """Create a new partenaire"""
        try:
            doc = self.db.create_document(
                self.COLLECTION_ID,
                {
                    'nom': nom,
                    'logo_url': logo_url,
                    'url': url or '',
                    'type_partenaire': type_partenaire,
                }
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error creating partenaire: {e}")
            raise
    
    def update(self, doc_id, **kwargs):
        """Update a partenaire"""
        try:
            doc = self.db.update_document(self.COLLECTION_ID, doc_id, kwargs)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error updating partenaire {doc_id}: {e}")
            raise
    
    def delete(self, doc_id):
        """Delete a partenaire"""
        try:
            return self.db.delete_document(self.COLLECTION_ID, doc_id)
        except Exception as e:
            logger.error(f"Error deleting partenaire {doc_id}: {e}")
            return False


class StatistiqueService(AppwriteService):
    """Service for Statistique operations"""
    
    COLLECTION_ID = 'statistiques'
    
    def list_all(self):
        """Get all statistiques, ordered by ordre"""
        try:
            docs = self.db.list_documents(
                self.COLLECTION_ID,
                queries=[Query.order_asc('ordre')]
            )
            return [self.to_dict(doc) for doc in docs]
        except Exception as e:
            logger.error(f"Error listing statistiques: {e}")
            return []
    
    def get_by_id(self, doc_id):
        """Get a statistique by ID"""
        try:
            doc = self.db.get_document(self.COLLECTION_ID, doc_id)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error getting statistique {doc_id}: {e}")
            return None
    
    def create(self, nom, valeur, icone, suffixe=None, ordre=0):
        """Create a new statistique"""
        try:
            doc = self.db.create_document(
                self.COLLECTION_ID,
                {
                    'nom': nom,
                    'valeur': valeur,
                    'suffixe': suffixe or '',
                    'icone': icone,
                    'ordre': ordre,
                }
            )
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error creating statistique: {e}")
            raise
    
    def update(self, doc_id, **kwargs):
        """Update a statistique"""
        try:
            doc = self.db.update_document(self.COLLECTION_ID, doc_id, kwargs)
            return self.to_dict(doc)
        except Exception as e:
            logger.error(f"Error updating statistique {doc_id}: {e}")
            raise
    
    def delete(self, doc_id):
        """Delete a statistique"""
        try:
            return self.db.delete_document(self.COLLECTION_ID, doc_id)
        except Exception as e:
            logger.error(f"Error deleting statistique {doc_id}: {e}")
            return False
