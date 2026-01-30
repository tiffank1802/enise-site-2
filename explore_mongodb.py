#!/usr/bin/env python3
import sys
sys.path.append('/root/enise-site')

import pymongo
from datetime import datetime

print("🗄️  EXPLORATEUR DE BASE DE DONNÉES MONGODB")
print("=============================================")

try:
    # Connexion à MongoDB
    client = pymongo.MongoClient(
        host='localhost',
        port=27017,
        username='tiffank1802',
        password='SzPLNg4zfgz3jKuF',
        authSource='admin'
    )
    
    db = client['enise_filesystem']
    
    print("✅ Connexion réussie à la base de données")
    print(f"📁 Base de données : enise_filesystem")
    print()
    
    # Lister les collections
    print("📋 Collections disponibles :")
    collections = db.list_collection_names()
    for i, collection in enumerate(collections, 1):
        print(f"   {i}. {collection}")
    print()
    
    # Contenu de file_metadata
    print("📁 Métadonnées des fichiers (file_metadata) :")
    try:
        files = list(db.file_metadata.find().limit(10))
        if files:
            print(f"   📊 Total fichiers : {db.file_metadata.count_documents({})}")
            print("   📄 10 derniers fichiers :")
            for i, file in enumerate(files, 1):
                filename = file.get('original_filename', file.get('filename', 'N/A'))
                size = file.get('file_size', 0)
                owner = file.get('owner_id', 'N/A')
                created = file.get('created_at', 'N/A')
                file_id = file.get('id', 'N/A')
                print(f"      {i}. {filename}")
                print(f"         ID: {file_id}")
                print(f"         Taille: {size} bytes")
                print(f"         Propriétaire: {owner}")
                print(f"         Créé: {created}")
                print()
        else:
            print("   Aucun fichier trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    print()
    
    # Contenu de fs.files (GridFS)
    print("📄 Fichiers GridFS (fs.files) :")
    try:
        gridfs_files = list(db.fs.files.find().limit(5))
        if gridfs_files:
            print(f"   📊 Total fichiers GridFS : {db.fs.files.count_documents({})}")
            print("   📄 5 premiers fichiers :")
            for i, file in enumerate(gridfs_files, 1):
                filename = file.get('filename', 'N/A')
                length = file.get('length', 0)
                upload_date = file.get('uploadDate', 'N/A')
                print(f"      {i}. {filename}")
                print(f"         Taille: {length} bytes")
                print(f"         Upload: {upload_date}")
                print()
        else:
            print("   Aucun fichier GridFS trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    print()
    
    # Logs d'accès
    print("📋 Logs d'accès (file_access_logs) :")
    try:
        logs = list(db.file_access_logs.find().sort('timestamp', -1).limit(5))
        if logs:
            print(f"   📊 Total logs : {db.file_access_logs.count_documents({})}")
            print("   📄 5 dernières activités :")
            for i, log in enumerate(logs, 1):
                file_id = log.get('file_id', 'N/A')
                user_id = log.get('user_id', 'N/A')
                access_type = log.get('access_type', 'N/A')
                timestamp = log.get('timestamp', 'N/A')
                success = log.get('success', True)
                status = "✅" if success else "❌"
                print(f"      {i}. [{status}] {access_type.upper()}")
                print(f"         Fichier: {file_id}")
                print(f"         Utilisateur: {user_id}")
                print(f"         Date: {timestamp}")
                print()
        else:
            print("   Aucun log trouvé")
    except Exception as e:
        print(f"   Erreur: {e}")
    print()
    
    # Statistiques de la base
    print("📊 Statistiques de la base de données :")
    try:
        stats = db.command('dbStats')
        print(f"   📦 Taille totale (bytes): {stats.get('dataSize', 0):,}")
        print(f"   📦 Taille totale (MB): {stats.get('dataSize', 0) / 1024 / 1024:.2f}")
        print(f"   📚 Collections: {len(collections)}")
        print(f"   📄 Index: {len(stats.get('indexes', []))}")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    client.close()
    print()
    print("🎯 Pour accéder manuellement :")
    print("   mongo --username tiffank1802 --password SzPLNg4zfgz3jKuF localhost:27017/enise_filesystem")
    print()
    
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
    print("Vérifiez que MongoDB est bien démarré")