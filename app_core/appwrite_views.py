from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from enise_site.appwrite_service import appwrite_db
from appwrite.query import Query
from appwrite.id import ID
import json


@csrf_exempt
@require_http_methods(["POST"])
def appwrite_create_document(request):
    """Créer un document dans une collection Appwrite"""
    try:
        data = json.loads(request.body)
        collection_id = data.pop('collection_id', None)
        
        if not collection_id:
            return JsonResponse({'success': False, 'error': 'collection_id requis'}, status=400)
        
        database = appwrite_db.get_database()
        document_id = data.get('document_id', ID.unique())
        
        result = database.create_document(
            database_id=appwrite_db.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
            data=data
        )
        
        return JsonResponse({'success': True, 'document': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def appwrite_list_documents(request):
    """Lister les documents d'une collection"""
    try:
        collection_id = request.GET.get('collection_id')
        queries = request.GET.getlist('queries', [])
        
        if not collection_id:
            return JsonResponse({'success': False, 'error': 'collection_id requis'}, status=400)
        
        database = appwrite_db.get_database()
        result = database.list_documents(
            database_id=appwrite_db.DATABASE_ID,
            collection_id=collection_id,
            queries=queries
        )
        
        return JsonResponse({'success': True, 'documents': result.get('documents', [])})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def appwrite_get_document(request, document_id):
    """Récupérer un document par son ID"""
    try:
        collection_id = request.GET.get('collection_id')
        
        if not collection_id:
            return JsonResponse({'success': False, 'error': 'collection_id requis'}, status=400)
        
        database = appwrite_db.get_database()
        result = database.get_document(
            database_id=appwrite_db.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id
        )
        
        return JsonResponse({'success': True, 'document': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def appwrite_update_document(request, document_id):
    """Mettre à jour un document"""
    try:
        data = json.loads(request.body)
        collection_id = data.pop('collection_id', None)
        
        if not collection_id:
            return JsonResponse({'success': False, 'error': 'collection_id requis'}, status=400)
        
        database = appwrite_db.get_database()
        result = database.update_document(
            database_id=appwrite_db.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
            data=data
        )
        
        return JsonResponse({'success': True, 'document': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def appwrite_delete_document(request, document_id):
    """Supprimer un document"""
    try:
        collection_id = request.GET.get('collection_id')
        
        if not collection_id:
            return JsonResponse({'success': False, 'error': 'collection_id requis'}, status=400)
        
        database = appwrite_db.get_database()
        database.delete_document(
            database_id=appwrite_db.DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id
        )
        
        return JsonResponse({'success': True, 'message': 'Document supprimé'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def appwrite_test_connection(request):
    """Tester la connexion Appwrite"""
    try:
        from django.conf import settings
        
        if not settings.APPWRITE_PROJECT_ID:
            return JsonResponse({
                'success': False, 
                'error': 'APPWRITE_PROJECT_ID non configuré'
            }, status=500)
        
        database = appwrite_db.get_database()
        result = database.list_documents(
            database_id=appwrite_db.DATABASE_ID,
            collection_id='specialites',
            queries=[Query.limit(1)]
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Connexion Appwrite établie',
            'endpoint': settings.APPWRITE_ENDPOINT,
            'project_id': settings.APPWRITE_PROJECT_ID
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)