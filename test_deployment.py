#!/usr/bin/env python
"""
Script de test pour vérifier le déploiement HF Spaces
Teste les endpoints critiques et la configuration Django
"""

import os
import sys
import django
from django.conf import settings
from django.test.client import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enise_site.settings')
django.setup()

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)

def test_configuration():
    """Test la configuration Django"""
    print_section("1. CONFIGURATION DJANGO")
    
    tests = [
        ("DEBUG", settings.DEBUG, False),
        ("ALLOWED_HOSTS", "*" in settings.ALLOWED_HOSTS, True),
        ("Secret Key défini", bool(settings.SECRET_KEY), True),
        ("Appwrite Endpoint", bool(settings.APPWRITE_ENDPOINT), True),
        ("WhiteNoise actif", "whitenoise" in str(settings.MIDDLEWARE).lower(), True),
    ]
    
    for name, value, expected in tests:
        status = "✓" if value == expected else "✗"
        print(f"{status} {name}: {value}")
        if value != expected:
            return False
    return True

def test_database():
    """Test la connexion à la base de données"""
    print_section("2. BASE DE DONNÉES")
    
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✓ Connexion à la base de données OK")
        return True
    except Exception as e:
        print(f"✗ Erreur de base de données: {e}")
        return False

def test_endpoints():
    """Test les endpoints principaux"""
    print_section("3. ENDPOINTS HTTP")
    
    client = Client()
    
    endpoints = [
        ("GET", "/", "Homepage"),
        ("GET", "/formations/", "Formations"),
        ("GET", "/admin/", "Admin"),
    ]
    
    all_ok = True
    for method, path, name in endpoints:
        try:
            if method == "GET":
                response = client.get(path)
            status_code = response.status_code
            status = "✓" if status_code < 500 else "✗"
            print(f"{status} {method} {path} [{status_code}] - {name}")
            if status_code >= 500:
                all_ok = False
        except Exception as e:
            print(f"✗ {method} {path} - Erreur: {e}")
            all_ok = False
    
    return all_ok

def test_appwrite():
    """Test la configuration Appwrite"""
    print_section("4. CONFIGURATION APPWRITE")
    
    configs = [
        ("APPWRITE_ENDPOINT", settings.APPWRITE_ENDPOINT),
        ("APPWRITE_PROJECT_ID", settings.APPWRITE_PROJECT_ID),
        ("APPWRITE_API_KEY", settings.APPWRITE_API_KEY[:10] + "***" if settings.APPWRITE_API_KEY else "NOT SET"),
        ("APPWRITE_DATABASE_ID", settings.APPWRITE_DATABASE_ID),
    ]
    
    all_ok = True
    for name, value in configs:
        is_set = value and value != "" and not value.endswith("***")
        status = "✓" if is_set else "⚠"
        display = value if not name.endswith("_KEY") else (value if is_set else "NOT SET")
        print(f"{status} {name}: {display}")
        if not is_set and "PROJECT_ID" in name:
            all_ok = False
    
    return all_ok

def test_static_files():
    """Test la configuration des fichiers statiques"""
    print_section("5. FICHIERS STATIQUES")
    
    checks = [
        ("STATIC_URL", settings.STATIC_URL),
        ("STATIC_ROOT", str(settings.STATIC_ROOT)),
        ("WhiteNoise Middleware", "whitenoise" in str(settings.MIDDLEWARE).lower()),
    ]
    
    for name, value in checks:
        if isinstance(value, bool):
            print(f"{'✓' if value else '✗'} {name}: {value}")
        else:
            print(f"✓ {name}: {value}")
    
    return True

def main():
    print("\n" + "="*60)
    print(" TEST DE DÉPLOIEMENT HF SPACES - ENISE SITE")
    print("="*60)
    
    results = {
        "Configuration Django": test_configuration(),
        "Base de données": test_database(),
        "Endpoints HTTP": test_endpoints(),
        "Appwrite": test_appwrite(),
        "Fichiers statiques": test_static_files(),
    }
    
    print_section("RÉSUMÉ DES TESTS")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "⚠ WARN"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests OK")
    
    if passed == total:
        print("\n✅ DÉPLOIEMENT PRÊT - Tous les tests sont passés!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) nécessite(nt) attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
