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
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    
    # Créer les données initiales si nécessaire
    try:
        execute_from_command_line(['manage.py', 'init_data'])
    except:
        pass
    
    # Démarrer gunicorn
    from gunicorn.app.wsgiapp import run
    sys.argv = [
        'gunicorn',
        'enise_site.wsgi',
        '--bind', '0.0.0.0:7860',
        '--workers', '2',
        '--timeout', '60',
        '--access-logfile', '-',
        '--error-logfile', '-'
    ]
    sys.exit(run())