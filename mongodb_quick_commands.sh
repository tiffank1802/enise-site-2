#!/bin/bash

echo "🔧 COMMANDES RAPIDES MONGODB"
echo "=========================="
echo ""

echo "📌 Se connecter à MongoDB :"
echo "   python -c \"
from pymongo import MongoClient
client = MongoClient('localhost', 27017, username='tiffank1802', password='SzPLNg4zfgz3jKuF')
db = client['enise_filesystem']
print('Collections:', db.list_collection_names())
print('Fichiers:', db.file_metadata.count_documents({}))
print('Logs:', db.file_access_logs.count_documents({}))
client.close()
\"
echo ""

echo "📋 Voir les fichiers récents :"
echo "   python explore_mongodb.py"
echo ""

echo "🗑️  Supprimer tous les fichiers (attention) :"
echo "   python -c \"
from pymongo import MongoClient
client = MongoClient('localhost', 27017, username='tiffank1802', password='SzPLNg4zfgz3jKuF')
db = client['enise_filesystem']
result = db.file_metadata.delete_many({})
result2 = db.file_access_logs.delete_many({})
print(f'Supprimé {result.deleted_count} fichiers et {result2.deleted_count} logs')
client.close()
\"
echo ""

echo "📊 Statistiques détaillées :"
echo "   python -c \"
from pymongo import MongoClient
client = MongoClient('localhost', 27017, username='tiffank1802', password='SzPLNg4zfgz3jKuF')
db = client['enise_filesystem']

# Taille par collection
for collection_name in db.list_collection_names():
    coll = db[collection_name]
    count = coll.count_documents({})
    stats = db.command('collStats', collection_name)
    size = stats.get('size', 0) / 1024  # en KB
    print(f'{collection_name}: {count} documents, {size:.2f} KB')

client.close()
\"
echo ""

echo "🌐 Interface web alternative :"
echo "   Si vous voulez une interface web simple, installez 'mongo-express':"
echo "   npm install -g mongo-express"
echo "   mongo-express -u tiffank1802 -p SzPLNg4zfgz3jKuF -d enise_filesystem"
echo "   Puis accédez à http://localhost:8081"
echo ""

echo "📋 Exécuter l'explorateur complet :"
echo "   source venv/bin/activate && python explore_mongodb.py"
echo ""