"""
Management command to seed initial data into Appwrite collections
"""

from django.core.management.base import BaseCommand
from app_core.services import (
    SpecialiteService,
    ActualiteService,
    StatistiqueService,
    PartenairesService,
)
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seed initial data into Appwrite collections'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding Appwrite collections...'))

        try:
            self.seed_specialites()
            self.seed_actualites()
            self.seed_statistiques()
            self.seed_partenaires()

            self.stdout.write(
                self.style.SUCCESS('✅ Data successfully seeded to Appwrite')
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Seeding failed: {e}'))
            logger.exception("Error seeding data")
            raise

    def seed_specialites(self):
        """Seed specialites collection"""
        service = SpecialiteService()
        
        specialites_data = [
            {
                'nom': 'Génie Civil',
                'description': 'Formation en génie civil et travaux publics',
                'image_url': 'https://via.placeholder.com/300x200?text=Genie+Civil',
                'icone': 'fa-building',
                'ordre': 1,
            },
            {
                'nom': 'Mécanique',
                'description': 'Études en mécanique et mécatronique',
                'image_url': 'https://via.placeholder.com/300x200?text=Mecanique',
                'icone': 'fa-cogs',
                'ordre': 2,
            },
            {
                'nom': 'Physique',
                'description': 'Enseignement en physique et sciences fondamentales',
                'image_url': 'https://via.placeholder.com/300x200?text=Physique',
                'icone': 'fa-atom',
                'ordre': 3,
            },
        ]
        
        for spec_data in specialites_data:
            try:
                # Check if already exists
                existing = service.get_by_slug(spec_data['nom'].lower().replace(' ', '-'))
                if existing:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ℹ️  Specialite '{spec_data['nom']}' already exists, skipping"
                        )
                    )
                    continue
                
                result = service.create(**spec_data)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Created specialite: {spec_data['nom']}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  Error creating {spec_data['nom']}: {e}")
                )

    def seed_actualites(self):
        """Seed actualites collection"""
        service = ActualiteService()
        
        actualites_data = [
            {
                'titre': 'Bienvenue à l\'ENISE',
                'contenu': 'Découvrez notre école d\'ingénieurs prestigieuse basée à Saint-Étienne.',
                'image_url': 'https://via.placeholder.com/600x400?text=Bienvenue',
                'est_publie': True,
            },
            {
                'titre': 'Événement scientifique 2024',
                'contenu': 'Participez à nos événements scientifiques tout au long de l\'année.',
                'image_url': 'https://via.placeholder.com/600x400?text=Evenement',
                'est_publie': True,
            },
            {
                'titre': 'Internships et stages',
                'contenu': 'Explorez les opportunités de stage dans des entreprises partenaires.',
                'image_url': 'https://via.placeholder.com/600x400?text=Stages',
                'est_publie': True,
            },
        ]
        
        for actu_data in actualites_data:
            try:
                # Check if already exists
                existing = service.get_by_slug(actu_data['titre'].lower().replace(' ', '-'))
                if existing:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  ℹ️  Actualite '{actu_data['titre']}' already exists, skipping"
                        )
                    )
                    continue
                
                result = service.create(**actu_data)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Created actualite: {actu_data['titre']}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  Error creating actualite: {e}")
                )

    def seed_statistiques(self):
        """Seed statistiques collection"""
        service = StatistiqueService()
        
        statistiques_data = [
            {
                'nom': 'Étudiants',
                'valeur': '1200',
                'suffixe': '+',
                'icone': 'fa-users',
                'ordre': 1,
            },
            {
                'nom': 'Années d\'existence',
                'valeur': '50',
                'suffixe': '+',
                'icone': 'fa-calendar',
                'ordre': 2,
            },
            {
                'nom': 'Entreprises partenaires',
                'valeur': '300',
                'suffixe': '+',
                'icone': 'fa-briefcase',
                'ordre': 3,
            },
        ]
        
        for stat_data in statistiques_data:
            try:
                # Check if already exists by trying to create
                result = service.create(**stat_data)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Created statistique: {stat_data['nom']}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  Error creating statistique: {e}")
                )

    def seed_partenaires(self):
        """Seed partenaires collection"""
        service = PartenairesService()
        
        partenaires_data = [
            {
                'nom': 'SNCF',
                'logo_url': 'https://via.placeholder.com/200x100?text=SNCF',
                'url': 'https://www.sncf.com',
                'type_partenaire': 'INDUSTRIEL',
            },
            {
                'nom': 'Université de Lyon',
                'logo_url': 'https://via.placeholder.com/200x100?text=UDL',
                'url': 'https://www.univ-lyon.fr',
                'type_partenaire': 'ACADEMIQUE',
            },
            {
                'nom': 'Région Auvergne-Rhône-Alpes',
                'logo_url': 'https://via.placeholder.com/200x100?text=Region',
                'url': 'https://www.auvergne-rhone-alpes.fr',
                'type_partenaire': 'INSTITUTIONNEL',
            },
        ]
        
        for partner_data in partenaires_data:
            try:
                result = service.create(**partner_data)
                self.stdout.write(
                    self.style.SUCCESS(f"  ✅ Created partenaire: {partner_data['nom']}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"  ⚠️  Error creating partenaire: {e}")
                )
