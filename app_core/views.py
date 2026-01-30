from django.shortcuts import render
from django.http import Http404
from .services import SpecialiteService, ActualiteService, StatistiqueService

specialite_service = SpecialiteService()
actualite_service = ActualiteService()
statistique_service = StatistiqueService()


def index(request):
    """Vue pour la page d'accueil"""
    specialites = specialite_service.list_all()
    actualites = actualite_service.list_published(limit=3)
    statistiques = statistique_service.list_all()
    
    context = {
        'specialites': specialites,
        'actualites': actualites,
        'statistiques': statistiques,
        'page_title': 'Accueil - ENISE',
    }
    return render(request, 'app_core/index.html', context)


def formations(request):
    """Vue pour la page des formations"""
    specialites = specialite_service.list_all()
    
    context = {
        'specialites': specialites,
        'page_title': 'Formations - ENISE',
    }
    return render(request, 'app_core/formations.html', context)


def specialite_detail(request, slug):
    """Vue pour le détail d'une spécialité"""
    specialite = specialite_service.get_by_slug(slug)
    
    if not specialite:
        raise Http404("Spécialité not found")
    
    context = {
        'specialite': specialite,
        'page_title': f'{specialite.get("nom", "Spécialité")} - ENISE',
    }
    return render(request, 'app_core/specialite_detail.html', context)
