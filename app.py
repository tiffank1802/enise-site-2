#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enise_site.settings')

if __name__ == '__main__':
    # Initialiser Django
    django.setup()
    
    # Créer les migrations
    try:
        execute_from_command_line(['app.py', 'migrate', '--noinput'])
        print("[INFO] Migrations completed successfully")
    except Exception as e:
        print(f"[WARNING] Migration error (non-critical): {e}")
    
    # Créer les données initiales si nécessaire
    try:
        execute_from_command_line(['app.py', 'init_data'])
        print("[INFO] Initial data loaded")
    except Exception as e:
        print(f"[INFO] No initial data command or already loaded: {e}")
    
    # Démarrer gunicorn
    print("[INFO] Starting gunicorn server on 0.0.0.0:7860")
    from gunicorn.app.wsgiapp import run
    sys.argv = [
        'gunicorn',
        'enise_site.wsgi',
        '--bind', '0.0.0.0:7860',
        '--workers', '2',
        '--timeout', '60',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info'
    ]
    sys.exit(run())