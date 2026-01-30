from django.shortcuts import render
from .models import Specialite, Actualite, Statistique

def index(request):
    """Vue pour la page d'accueil"""
    specialites = Specialite.objects.all()
    actualites = Actualite.objects.filter(est_publie=True)[:3]
    
    context = {
        'specialites': specialites,
        'actualites': actualites,
        'page_title': 'Accueil - ENISE',
    }
    return render(request, 'core/index.html', context)

def formations(request):
    """Vue pour la page des formations"""
    specialites = Specialite.objects.all()
    
    context = {
        'specialites': specialites,
        'page_title': 'Formations - ENISE',
    }
    return render(request, 'core/formations.html', context)
