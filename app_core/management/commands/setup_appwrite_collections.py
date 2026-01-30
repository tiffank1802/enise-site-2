"""
Management command to setup Appwrite collections with proper schema
This replaces Django models with Appwrite database structure
"""

from django.core.management.base import BaseCommand
from enise_site.appwrite_db import get_appwrite_db
from appwrite.services.databases import Databases
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create Appwrite collections for ENISE website'

    def handle(self, *args, **options):
        db = get_appwrite_db()
        
        # Test connection first
        if not db.test_connection():
            self.stdout.write(
                self.style.ERROR('❌ Cannot connect to Appwrite')
            )
            return

        self.stdout.write(self.style.SUCCESS('✅ Connected to Appwrite'))

        # Create collections
        self.create_specialites_collection(db)
        self.create_actualites_collection(db)
        self.create_contact_collection(db)
        self.create_partenaires_collection(db)
        self.create_statistiques_collection(db)

        self.stdout.write(
            self.style.SUCCESS('✅ All Appwrite collections configured')
        )

    def create_specialites_collection(self, db):
        """Create specialites collection"""
        collection_id = 'specialites'
        attributes = [
            {
                'key': 'nom',
                'type': 'string',
                'size': 100,
                'required': True,
            },
            {
                'key': 'slug',
                'type': 'string',
                'size': 100,
                'required': True,
            },
            {
                'key': 'description',
                'type': 'string',
                'size': 65535,
                'required': True,
            },
            {
                'key': 'image_url',
                'type': 'url',
                'required': False,
            },
            {
                'key': 'icone',
                'type': 'string',
                'size': 50,
                'required': False,
            },
            {
                'key': 'ordre',
                'type': 'integer',
                'required': True,
                'default': 0,
            },
        ]
        
        try:
            db.create_collection(collection_id, 'Spécialités ENISE', attributes)
            self.stdout.write(
                self.style.SUCCESS(f'  ✅ Collection {collection_id} created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {collection_id}: {e}')
            )

    def create_actualites_collection(self, db):
        """Create actualites collection"""
        collection_id = 'actualites'
        attributes = [
            {
                'key': 'titre',
                'type': 'string',
                'size': 200,
                'required': True,
            },
            {
                'key': 'slug',
                'type': 'string',
                'size': 200,
                'required': True,
            },
            {
                'key': 'contenu',
                'type': 'string',
                'size': 65535,
                'required': True,
            },
            {
                'key': 'image_url',
                'type': 'url',
                'required': False,
            },
            {
                'key': 'date_publication',
                'type': 'datetime',
                'required': True,
            },
            {
                'key': 'est_publie',
                'type': 'boolean',
                'required': True,
                'default': True,
            },
        ]
        
        try:
            db.create_collection(collection_id, 'Actualités', attributes)
            self.stdout.write(
                self.style.SUCCESS(f'  ✅ Collection {collection_id} created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {collection_id}: {e}')
            )

    def create_contact_collection(self, db):
        """Create contact collection"""
        collection_id = 'contact'
        attributes = [
            {
                'key': 'nom',
                'type': 'string',
                'size': 100,
                'required': True,
            },
            {
                'key': 'email',
                'type': 'email',
                'required': True,
            },
            {
                'key': 'sujet',
                'type': 'string',
                'size': 200,
                'required': True,
            },
            {
                'key': 'message',
                'type': 'string',
                'size': 65535,
                'required': True,
            },
            {
                'key': 'date_envoi',
                'type': 'datetime',
                'required': True,
            },
            {
                'key': 'traite',
                'type': 'boolean',
                'required': True,
                'default': False,
            },
        ]
        
        try:
            db.create_collection(collection_id, 'Messages de Contact', attributes)
            self.stdout.write(
                self.style.SUCCESS(f'  ✅ Collection {collection_id} created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {collection_id}: {e}')
            )

    def create_partenaires_collection(self, db):
        """Create partenaires collection"""
        collection_id = 'partenaires'
        attributes = [
            {
                'key': 'nom',
                'type': 'string',
                'size': 150,
                'required': True,
            },
            {
                'key': 'logo_url',
                'type': 'url',
                'required': True,
            },
            {
                'key': 'url',
                'type': 'url',
                'required': False,
            },
            {
                'key': 'type_partenaire',
                'type': 'string',
                'size': 50,
                'required': True,
            },
        ]
        
        try:
            db.create_collection(collection_id, 'Partenaires', attributes)
            self.stdout.write(
                self.style.SUCCESS(f'  ✅ Collection {collection_id} created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {collection_id}: {e}')
            )

    def create_statistiques_collection(self, db):
        """Create statistiques collection"""
        collection_id = 'statistiques'
        attributes = [
            {
                'key': 'nom',
                'type': 'string',
                'size': 100,
                'required': True,
            },
            {
                'key': 'valeur',
                'type': 'string',
                'size': 50,
                'required': True,
            },
            {
                'key': 'suffixe',
                'type': 'string',
                'size': 10,
                'required': False,
            },
            {
                'key': 'icone',
                'type': 'string',
                'size': 50,
                'required': True,
            },
            {
                'key': 'ordre',
                'type': 'integer',
                'required': True,
                'default': 0,
            },
        ]
        
        try:
            db.create_collection(collection_id, 'Statistiques', attributes)
            self.stdout.write(
                self.style.SUCCESS(f'  ✅ Collection {collection_id} created')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  ⚠️  {collection_id}: {e}')
            )
