#!/usr/bin/env python
"""Vérifie les variables d'environnement configurées"""

import os
from pathlib import Path

print("\n" + "="*60)
print(" VÉRIFICATION DES VARIABLES D'ENVIRONNEMENT")
print("="*60)

# Variables critiques
critical_vars = [
    "DEBUG",
    "SECRET_KEY",
    "ALLOWED_HOSTS",
    "APPWRITE_ENDPOINT",
    "APPWRITE_PROJECT_ID",
    "APPWRITE_API_KEY",
    "APPWRITE_DATABASE_ID",
]

print("\n🔍 Variables d'environnement actuelles:\n")

missing = []
set_vars = []

for var in critical_vars:
    value = os.environ.get(var, "")
    if value:
        # Masquer les valeurs sensibles
        if "KEY" in var or "PASSWORD" in var:
            display = value[:10] + "***" if len(value) > 10 else "***"
        else:
            display = value[:50] + "..." if len(value) > 50 else value
        print(f"✓ {var:<30} = {display}")
        set_vars.append(var)
    else:
        print(f"✗ {var:<30} = [NOT SET]")
        missing.append(var)

print(f"\n📊 Résumé:")
print(f"   • Configurées: {len(set_vars)}/{len(critical_vars)}")
print(f"   • Manquantes: {len(missing)}/{len(critical_vars)}")

if missing:
    print(f"\n⚠️  Variables manquantes:")
    for var in missing:
        print(f"   - {var}")

# Vérifier le fichier .env local
print(f"\n📝 Fichier .env local:")
env_file = Path("/root/enise-site/.env")
if env_file.exists():
    print(f"✓ Fichier .env trouvé")
    with open(env_file) as f:
        lines = f.readlines()
    print(f"   {len(lines)} lignes dans le fichier")
else:
    print(f"✗ Fichier .env non trouvé")

print("\n" + "="*60)
