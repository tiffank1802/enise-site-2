from django.core.management.base import BaseCommand
from app_core.models import Specialite, Statistique, Actualite

class Command(BaseCommand):
    help = 'Initialise les données par défaut'
    
    def handle(self, *args, **options):
        # Supprimer les anciennes données
        Specialite.objects.all().delete()
        Statistique.objects.all().delete()
        Actualite.objects.all().delete()
        
        # Ajouter les spécialités
        specialites = [
            {
                'nom': 'Génie Civil',
                'description': 'Formation complète en ingénierie de la construction : bâtiment, travaux publics, ouvrages d\'art, et énergétique du bâtiment. Cette spécialité prépare les futurs ingénieurs à concevoir, construire et gérer les infrastructures de demain.',
                'icone': 'fa-building',
                'ordre': 0
            },
            {
                'nom': 'Génie Mécanique',
                'description': 'Expertise en conception mécanique, productique, énergétique et matériaux. Les étudiants apprennent à concevoir des systèmes mécaniques innovants, optimiser les processus de production et maîtriser les nouveaux matériaux.',
                'icone': 'fa-cogs',
                'ordre': 1
            },
            {
                'nom': 'Génie Physique',
                'description': 'Spécialisation à l\'interface de la physique et de l\'ingénierie : capteurs communicants, photonique, instrumentation scientifique. Formation orientée vers les hautes technologies et la recherche.',
                'icone': 'fa-atom',
                'ordre': 2
            }
        ]
        
        for spec_data in specialites:
            specialite = Specialite(**spec_data)
            specialite.save()
        
        # Ajouter les statistiques
        statistiques = [
            {'nom': 'Étudiants', 'valeur': '1000', 'suffixe': '+', 'icone': 'fa-users', 'ordre': 0},
            {'nom': 'Ans d\'expérience', 'valeur': '60', 'suffixe': '', 'icone': 'fa-calendar', 'ordre': 1},
            {'nom': 'Embauche à 6 mois', 'valeur': '90', 'suffixe': '%', 'icone': 'fa-briefcase', 'ordre': 2},
            {'nom': 'Partenariats', 'valeur': '120', 'suffixe': '+', 'icone': 'fa-handshake', 'ordre': 3}
        ]
        
        for stat_data in statistiques:
            statistique = Statistique(**stat_data)
            statistique.save()
        
        # Ajouter quelques actualités
        actualites = [
            {
                'titre': 'Nouveau laboratoire de recherche en matériaux composites',
                'slug': 'nouveau-laboratoire-materiaux-composites',
                'contenu': 'L\'ENISE inaugure un nouveau laboratoire de pointe dédié à la recherche sur les matériaux composites. Ce nouvel équipement permettra de développer des innovations majeures dans les domaines de l\'aéronautique et de l\'automobile.',
                'est_publie': True
            },
            {
                'titre': 'Partenariat stratégique avec Airbus',
                'slug': 'partenariat-airbus',
                'contenu': 'Signature d\'un accord de partenariat majeur avec Airbus pour développer des programmes de formation conjoints et des projets de recherche en ingénierie aéronautique.',
                'est_publie': True
            },
            {
                'titre': 'Victoire au concours international d\'innovation',
                'slug': 'victoire-concours-innovation',
                'contenu': 'Une équipe d\'étudiants de l\'ENISE remporte le premier prix au concours international d\'innovation technologique avec leur projet de drones autonomes pour l\'inspection d\'ouvrages d\'art.',
                'est_publie': True
            }
        ]
        
        for actu_data in actualites:
            actualite = Actualite(**actu_data)
            actualite.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Données initiales créées avec succès !'))
        self.stdout.write(self.style.SUCCESS(f'✅ {len(specialites)} spécialités créées'))
        self.stdout.write(self.style.SUCCESS(f'✅ {len(statistiques)} statistiques créées'))
        self.stdout.write(self.style.SUCCESS(f'✅ {len(actualites)} actualités créées'))