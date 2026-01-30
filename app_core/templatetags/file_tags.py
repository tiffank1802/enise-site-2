# Filtres de templates personnalisés
from django import template

register = template.Library()

@register.filter
def file_icon(file_obj):
    """Retourner l'icône FontAwesome selon le type de fichier"""
    if not file_obj:
        return 'fa-file'
    
    # Si c'est un dictionnaire (depuis notre système de fichiers simple)
    if isinstance(file_obj, dict):
        filename = file_obj.get('original_filename', '') or file_obj.get('filename', '')
    else:
        filename = str(file_obj)
    
    filename = filename.lower()
    if filename.endswith('.pdf'):
        return 'fa-file-pdf'
    elif filename.endswith(('.doc', '.docx')):
        return 'fa-file-word'
    elif filename.endswith(('.xls', '.xlsx')):
        return 'fa-file-excel'
    elif filename.endswith(('.ppt', '.pptx')):
        return 'fa-file-powerpoint'
    elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        return 'fa-file-image'
    elif filename.endswith(('.mp4', '.avi', '.mov', '.wmv')):
        return 'fa-file-video'
    elif filename.endswith(('.mp3', '.wav', '.flac', '.aac')):
        return 'fa-file-audio'
    elif filename.endswith(('.zip', '.rar', '.7z', '.tar', '.gz')):
        return 'fa-file-archive'
    elif filename.endswith(('.txt', '.md')):
        return 'fa-file-alt'
    elif filename.endswith(('.py', '.js', '.html', '.css', '.java', '.cpp')):
        return 'fa-file-code'
    else:
        return 'fa-file'

@register.filter
def filesizeformat(size_value):
    """Formater la taille des fichiers"""
    if not size_value:
        return '0 B'
    
    # Si c'est déjà une chaîne formatée, la retourner
    if isinstance(size_value, str):
        return size_value
    
    bytes_value = int(size_value)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"