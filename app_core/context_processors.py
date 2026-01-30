from .models import Statistique

def statistiques(request):
    """Inclut les statistiques dans tous les templates"""
    return {
        'statistiques': Statistique.objects.all().order_by('ordre')
    }