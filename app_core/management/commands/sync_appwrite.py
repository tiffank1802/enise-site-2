from django.core.management.base import BaseCommand
from django.conf import settings
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from app_core.models import Specialite, Actualite, Contact, Partenaire, Statistique


class Command(BaseCommand):
    help = 'Sync data with Appwrite'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Test connection only')

    def handle(self, *args, **options):
        if not settings.APPWRITE_PROJECT_ID or not settings.APPWRITE_API_KEY:
            self.stdout.write(self.style.ERROR(
                'Variables APPWRITE_PROJECT_ID et APPWRITE_API_KEY requises dans .env'
            ))
            return

        client = Client()
        client.set_endpoint(settings.APPWRITE_ENDPOINT)
        client.set_project(settings.APPWRITE_PROJECT_ID)
        client.set_key(settings.APPWRITE_API_KEY)

        databases = Databases(client)
        database_id = settings.APPWRITE_DATABASE_ID

        if options['test']:
            try:
                result = databases.list_documents(database_id, 'specialites', [], 1, 0)
                self.stdout.write(self.style.SUCCESS('Connexion Appwrite OK'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erreur: {e}'))
            return

        self.stdout.write('Synchronisation des données avec Appwrite...')

        for model, collection_id, fields in [
            (Specialite, 'specialites', ['nom', 'slug', 'description', 'image_url', 'icone', 'ordre']),
            (Actualite, 'actualites', ['titre', 'slug', 'contenu', 'image', 'date_publication', 'est_publie']),
            (Contact, 'contact', ['nom', 'email', 'sujet', 'message', 'date_envoi', 'traite']),
            (Partenaire, 'partenaires', ['nom', 'logo', 'url', 'type_partenaire']),
            (Statistique, 'statistiques', ['nom', 'valeur', 'suffixe', 'icone', 'ordre']),
        ]:
            count = 0
            for obj in model.objects.all():
                data = {field: getattr(obj, field) for field in fields if hasattr(obj, field)}
                data['django_id'] = obj.id
                try:
                    databases.create_document(database_id, collection_id, data)
                    count += 1
                except Exception:
                    pass
            self.stdout.write(f'{model.__name__}: {count} documents synchronisés')

        self.stdout.write(self.style.SUCCESS('Sync terminée!'))