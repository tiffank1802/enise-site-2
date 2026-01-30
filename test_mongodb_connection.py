#!/usr/bin/env python

import os
import sys

# Ajouter le path du projet
sys.path.append('/root/enise-site')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'enise_site.settings')

import django
django.setup()

# Test de la connexion MongoDB
print("🧪 TEST DE CONNEXION MONGODB")
print("===============================")

try:
    from simple_file_services import file_manager
    
    print(f"✅ Service de fichiers initialisé")
    print(f"📊 Utilisation MongoDB : {file_manager.use_mongodb}")
    
    if file_manager.use_mongodb:
        print(f"🔗 Client MongoDB : {type(file_manager.client)}")
        print(f"📁 Base de données : {file_manager.db.name if hasattr(file_manager, 'db') else 'N/A'}")
        print(f"📋 Collections disponibles : {file_manager.db.list_collection_names() if hasattr(file_manager, 'db') else 'N/A'}")
    else:
        print("⚠️ Utilisation du fallback (fichiers locaux)")
        
    print("\n🎯 Test d'upload...")
    
    # Créer un petit fichier de test
    random_data = str(os.urandom(8))
    test_content = b"Fichier de test pour MongoDB - " + random_data.encode()
    from io import BytesIO
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    test_file = SimpleUploadedFile("test_mongodb.txt", test_content)
    
    # Test upload
    result = file_manager.upload_file(
        file_data=test_file,
        filename="test_mongodb.txt",
        user_id="test_user",
        is_public=False,
        tags=["test", "mongodb"]
    )
    
    print(f"📤 Résultat upload : {result}")
    
    if result['success']:
        # Test list
        files = file_manager.list_files("test_user")
        print(f"📋 Fichiers trouvés : {len(files)}")
        
        if files:
            print(f"📄 Premier fichier : {files[0]['filename']}")
            print(f"📊 Taille : {files[0]['file_size']} bytes")
            print(f"🔐 Hash : {files[0]['file_hash'][:16]}...")
    
    print("\n✅ Test terminé avec succès!")
    
except Exception as e:
    print(f"❌ Erreur : {e}")
    import traceback
    traceback.print_exc()