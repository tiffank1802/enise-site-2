# Script pour créer l'utilisateur MongoDB
import sys
sys.path.append('/opt/mongodb-linux-aarch64-ubuntu2204-7.0.9/bin')

from pymongo import MongoClient

# Connexion sans authentification
client = MongoClient('localhost', 27017)

# Créer l'utilisateur dans la base de données admin
try:
    db = client.admin
    
    # Créer l'utilisateur tiffank1802
    db.command("createUser", "tiffank1802", pwd="SzPLNg4zfgz3jKuF", roles=[
        {"role": "readWrite", "db": "enise_filesystem"},
        {"role": "readWrite", "db": "enise_db"}
    ])
    
    print("✅ Utilisateur MongoDB créé avec succès !")
    print(f"👤 Nom: tiffank1802")
    print(f"🔐 Roles: readWrite sur enise_filesystem et enise_db")
    
except Exception as e:
    print(f"❌ Erreur: {e}")

finally:
    client.close()