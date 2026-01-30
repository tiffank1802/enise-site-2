#!/bin/bash

echo "🗄️  ACCÈS AU CONTENU DE VOTRE BASE DE DONNÉES MONGODB"
echo "======================================================"
echo ""
echo "🔐 Vos identifiants :"
echo "   • Utilisateur : tiffank1802"
echo "   • Mot de passe : SzPLNg4zfgz3jKuF"
echo "   • Hôte : localhost:27017"
echo "   • Base : enise_filesystem"
echo ""

echo "📋 MÉTHODE 1 : Ligne de commande (mongo shell)"
echo "------------------------------------------------"
echo "Connectez-vous avec :"
echo "/opt/mongodb-linux-aarch64-ubuntu2204-7.0.9/bin/mongo --username tiffank1802 --password SzPLNg4zfgz3jKuF localhost:27017/enise_filesystem"
echo ""
echo "Commandes utiles une fois connecté :"
echo "   show collections                    # Voir toutes les collections"
echo "   db.file_metadata.find()           # Voir tous les fichiers"
echo "   db.fs.files.find()               # Voir les fichiers GridFS"
echo "   db.file_access_logs.find()         # Voir les logs d'accès"
echo "   db.stats()                       # Statistiques de la base"
echo ""

echo "📋 MÉTHODE 2 : Commandes directes"
echo "----------------------------------------"
echo "Voir les collections :"
echo "/opt/mongodb-linux-aarch64-ubuntu2204-7.0.9/bin/mongo --username tiffank1802 --password SzPLNg4zfgz3jKuF localhost:27017/enise_filesystem --eval 'show collections'"
echo ""
echo "Compter les fichiers :"
echo "/opt/mongodb-linux-aarch64-ubuntu2204-7.0.9/bin/mongo --username tiffank1802 --password SzPLNg4zfgz3jKuF localhost:27017/enise_filesystem --eval 'db.file_metadata.count()'"
echo ""

echo "📋 MÉTHODE 3 : Python (avec pymongo)"
echo "----------------------------------------"
echo "Créer un script Python pour explorer :"
cat << 'EOF'
# explore_mongodb.py
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient(
    host='localhost',
    port=27017,
    username='tiffank1802',
    password='SzPLNg4zfgz3jKuF'
)

db = client['enise_filesystem']

print("📊 Collections dans la base de données :")
collections = db.list_collection_names()
for collection in collections:
    print(f"  • {collection}")

print("\n📁 Contenu de file_metadata :")
files = list(db.file_metadata.find().limit(5))
for file in files:
    print(f"  • {file.get('filename', 'N/A')} - {file.get('file_size', 0)} bytes - {file.get('owner_id', 'N/A')}")

print(f"\n📈 Total fichiers : {db.file_metadata.count_documents({})}")
print(f"📋 Total logs : {db.file_access_logs.count_documents({})}")

client.close()
EOF

echo "Exécutez avec : source venv/bin/activate && python explore_mongodb.py"
echo ""

echo "📋 MÉTHODE 4 : Interface web (si disponible)"
echo "------------------------------------------------"
echo "Si vous avez MongoDB Compass ou Studio 3T :"
echo "   • Connection String : mongodb://tiffank1802:SzPLNg4zfgz3jKuF@localhost:27017/enise_filesystem"
echo "   • Host : localhost"
echo "   • Port : 27017"
echo "   • Username : tiffank1802"
echo "   • Password : SzPLNg4zfgz3jKuF"
echo "   • Database : enise_filesystem"
echo ""

echo "🔍 Je vais maintenant exécuter quelques requêtes pour vous..."