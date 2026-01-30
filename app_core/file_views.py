# Vues Django pour la gestion des fichiers (version simplifiée)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
import json
from simple_file_services import file_manager

def file_manager_view(request):
    """Vue principale du gestionnaire de fichiers"""
    user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
    
    # Récupérer les fichiers de l'utilisateur
    files = file_manager.list_files(user_id)
    
    # Regrouper par catégorie
    files_by_category = {}
    for file in files:
        category = file.get('category', 'other')
        if category not in files_by_category:
            files_by_category[category] = []
        files_by_category[category].append(file)
    
    context = {
        'files': files,
        'files_by_category': files_by_category,
        'total_files': len(files),
        'page_title': 'Gestionnaire de fichiers - ENISE'
    }
    
    return render(request, 'app_core/file_manager.html', context)

@login_required
@require_http_methods(['POST'])
@csrf_exempt
def upload_file(request):
    """Uploader un fichier"""
    if request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
        
        # Paramètres supplémentaires
        is_public = request.POST.get('is_public', 'false').lower() == 'true'
        tags = request.POST.getlist('tags', [])
        
        # Uploader le fichier
        result = file_manager.upload_file(
            file_data=uploaded_file,
            filename=uploaded_file.name,
            user_id=user_id,
            is_public=is_public,
            tags=tags
        )
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'file_id': result['file_id'],
                'message': result['message']
            })
        else:
            return JsonResponse({
                'success': False,
                'message': result['message']
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'No file provided'}, status=400)

@login_required
def download_file(request, file_id):
    """Télécharger un fichier"""
    try:
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
        
        # Récupérer le fichier
        result = file_manager.get_file(file_id, user_id)
        
        if not result:
            return JsonResponse({'success': False, 'message': 'File not found or access denied'}, status=404)
        
        file_data, metadata = result
        
        # Créer la réponse HTTP
        response = HttpResponse(file_data, content_type=metadata.get('mime_type', 'application/octet-stream'))
        response['Content-Disposition'] = f'attachment; filename="{metadata["original_filename"]}"'
        response['Content-Length'] = str(metadata.get('file_size', 0))
        
        return response
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(['DELETE'])
@csrf_exempt
def delete_file(request, file_id):
    """Supprimer un fichier"""
    try:
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
        
        # Vérifier si l'utilisateur est admin
        is_admin = request.user.is_staff if hasattr(request.user, 'is_staff') else False
        
        # Supprimer le fichier
        success = file_manager.delete_file(file_id, user_id, is_admin)
        
        if success:
            return JsonResponse({'success': True, 'message': 'File deleted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to delete file'}, status=400)
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
@require_http_methods(['POST'])
@csrf_exempt
def grant_access(request, file_id):
    """Donner l'accès à un fichier"""
    try:
        data = json.loads(request.body)
        user_ids = data.get('user_ids', [])
        
        # Pour l'instant, retourner success car cette fonctionnalité sera implémentée plus tard
        return JsonResponse({'success': True, 'message': 'Access granted successfully'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def file_details(request, file_id):
    """Afficher les détails d'un fichier"""
    try:
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
        
        # Récupérer les métadonnées
        files = file_manager.list_files(user_id)
        metadata = None
        for file_meta in files:
            if file_meta.get('id') == file_id:
                metadata = file_meta
                break
        
        if not metadata:
            return JsonResponse({'success': False, 'message': 'File not found or access denied'}, status=404)
        
        # Récupérer les logs d'accès
        logs = file_manager.get_access_logs(file_id, user_id)
        
        context = {
            'file': metadata,
            'logs': logs,
            'page_title': f'Détails du fichier - {metadata["original_filename"]}'
        }
        
        return render(request, 'app_core/file_details.html', context)
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def access_logs(request):
    """Afficher les logs d'accès"""
    user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
    
    # Récupérer les logs de l'utilisateur
    logs = file_manager.get_access_logs(user_id=user_id)
    
    context = {
        'logs': logs,
        'total_logs': len(logs),
        'page_title': 'Logs d\'accès - ENISE'
    }
    
    return render(request, 'app_core/access_logs.html', context)