from django.core.management.base import BaseCommand
from app_core.models import Specialite

class Command(BaseCommand):
    help = 'Initialize database with sample data'

    def handle(self, *args, **options):
        # Create default specialties if they don't exist
        if Specialite.objects.exists():
            self.stdout.write(self.style.SUCCESS('Database already initialized'))
            return
        
        specialities = [
            {
                'nom': 'Génie Civil',
                'slug': 'genie-civil',
                'description': 'Conception et construction d\'ouvrages',
                'icone': 'fa-building',
                'ordre': 1
            },
            {
                'nom': 'Mécanique',
                'slug': 'mecanique',
                'description': 'Ingénierie mécanique et design',
                'icone': 'fa-cog',
                'ordre': 2
            },
            {
                'nom': 'Physique',
                'slug': 'physique',
                'description': 'Physique appliquée et recherche',
                'icone': 'fa-atom',
                'ordre': 3
            },
        ]
        
        for spec_data in specialities:
            Specialite.objects.create(**spec_data)
            self.stdout.write(self.style.SUCCESS(f'Created: {spec_data["nom"]}'))
        
        self.stdout.write(self.style.SUCCESS('Database initialized successfully!'))
