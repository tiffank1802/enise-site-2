from django.core.management.base import BaseCommand
from django.conf import settings
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query


class Command(BaseCommand):
    help = 'Configure Appwrite database and collections'

    def handle(self, *args, **options):
        client = Client()
        client.set_endpoint(settings.APPWRITE_ENDPOINT)
        client.set_project(settings.APPWRITE_PROJECT_ID)
        client.set_key(settings.APPWRITE_API_KEY)

        databases = Databases(client)
        database_id = settings.APPWRITE_DATABASE_ID

        self.stdout.write(f'Configuration Appwrite pour la base: {database_id}')

        collections = [
            {
                'name': 'specialites',
                'id': 'specialites',
                'attributes': [
                    {'key': 'nom', 'type': 'string', 'size': 100, 'required': True},
                    {'key': 'slug', 'type': 'string', 'size': 100, 'required': True},
                    {'key': 'description', 'type': 'string', 'size': 5000, 'required': True},
                    {'key': 'image_url', 'type': 'string', 'size': 500, 'required': False},
                    {'key': 'icone', 'type': 'string', 'size': 50, 'required': False},
                    {'key': 'ordre', 'type': 'integer', 'required': False},
                ]
            },
            {
                'name': 'actualites',
                'id': 'actualites',
                'attributes': [
                    {'key': 'titre', 'type': 'string', 'size': 200, 'required': True},
                    {'key': 'slug', 'type': 'string', 'size': 200, 'required': True},
                    {'key': 'contenu', 'type': 'string', 'size': 50000, 'required': True},
                    {'key': 'image_url', 'type': 'string', 'size': 500, 'required': False},
                    {'key': 'date_publication', 'type': 'datetime', 'required': True},
                    {'key': 'est_publie', 'type': 'boolean', 'required': True},
                ]
            },
            {
                'name': 'contact',
                'id': 'contact',
                'attributes': [
                    {'key': 'nom', 'type': 'string', 'size': 100, 'required': True},
                    {'key': 'email', 'type': 'string', 'size': 200, 'required': True},
                    {'key': 'sujet', 'type': 'string', 'size': 200, 'required': True},
                    {'key': 'message', 'type': 'string', 'size': 10000, 'required': True},
                    {'key': 'date_envoi', 'type': 'datetime', 'required': True},
                    {'key': 'traite', 'type': 'boolean', 'required': True},
                ]
            },
            {
                'name': 'partenaires',
                'id': 'partenaires',
                'attributes': [
                    {'key': 'nom', 'type': 'string', 'size': 150, 'required': True},
                    {'key': 'logo_url', 'type': 'string', 'size': 500, 'required': False},
                    {'key': 'url', 'type': 'string', 'size': 500, 'required': False},
                    {'key': 'type_partenaire', 'type': 'string', 'size': 50, 'required': True},
                ]
            },
            {
                'name': 'statistiques',
                'id': 'statistiques',
                'attributes': [
                    {'key': 'nom', 'type': 'string', 'size': 100, 'required': True},
                    {'key': 'valeur', 'type': 'string', 'size': 50, 'required': True},
                    {'key': 'suffixe', 'type': 'string', 'size': 10, 'required': False},
                    {'key': 'icone', 'type': 'string', 'size': 50, 'required': False},
                    {'key': 'ordre', 'type': 'integer', 'required': False},
                ]
            },
        ]

        for coll in collections:
            try:
                self.stdout.write(f'Création de la collection: {coll["name"]}')
                databases.create_collection(
                    database_id=database_id,
                    collection_id=coll['id'],
                    name=coll['name'],
                )
                self.stdout.write(self.style.SUCCESS(f'Collection {coll["name"]} créée'))

                for attr in coll['attributes']:
                    attr_type = attr['type']
                    if attr_type == 'string':
                        databases.create_string_attribute(
                            database_id, coll['id'], attr['key'], attr['size'], attr.get('required', False)
                        )
                    elif attr_type == 'integer':
                        databases.create_integer_attribute(
                            database_id, coll['id'], attr['key'], attr.get('required', False)
                        )
                    elif attr_type == 'boolean':
                        databases.create_boolean_attribute(
                            database_id, coll['id'], attr['key'], attr.get('required', False)
                        )
                    elif attr_type == 'datetime':
                        databases.create_datetime_attribute(
                            database_id, coll['id'], attr['key'], attr.get('required', False)
                        )
                    self.stdout.write(f'  Attribut {attr["key"]} ajouté')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Collection {coll["name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Configuration Appwrite terminée!'))