🗄️ CONFIGURATION MONGODB DANS VS CODE
====================================

🔧 INSTALLATION DE L'EXTENSION :
1. Ouvrez VS Code
2. Allez dans Extensions (Ctrl+Shift+X)
3. Recherchez "MongoDB"
4. Installez l'extension officielle "MongoDB for VS Code"

🔗 CONNEXION À VOTRE BASE :
1. Cliquez sur l'icône MongoDB dans la barre latérale gauche
2. Cliquez sur "Add Connection"
3. Remplissez les informations suivantes :

📋 CONNECTION STRING :
mongodb://tiffank1802:SzPLNg4zfgz3jKuF@localhost:27017/enise_filesystem

OU remplir manuellement :
• Connection Name: ENISE MongoDB
• Host: localhost
• Port: 27017
• Authentication: Username/Password
• Username: tiffank1802
• Password: SzPLNg4zfgz3jKuF
• Database: enise_filesystem

🎯 APRÈS CONNEXION VOUS VERREZ :
✅ enise_filesystem (base de données principale)
  📁 file_metadata (métadonnées des fichiers)
  📁 fs.files (fichiers GridFS)
  📁 fs.chunks (chunks de fichiers)
  📁 file_access_logs (logs d'accès)

📊 EXPLORATION DES DONNÉES :

1️⃣ Voir les fichiers uploadés :
   • Cliquez sur file_metadata
   • Vous verrez vos fichiers avec métadonnées
   • Chaque document contient : id, filename, file_size, owner_id, etc.

2️⃣ Voir les logs d'accès :
   • Cliquez sur file_access_logs
   • Vous verrez toutes les activités (upload, download, view, delete)
   • Avec timestamps, user_id, file_id, access_type

3️⃣ Voir les fichiers stockés :
   • Cliquez sur fs.files
   • Contient les fichiers réels stockés dans GridFS
   • Avec filename, length, uploadDate, metadata

🔍 REQUÊTES UTILES DANS VS CODE :

# Voir tous les fichiers récents
db.file_metadata.find().sort({"created_at": -1})

# Voir les fichiers par utilisateur
db.file_metadata.find({"owner_id": "test_user"})

# Voir les logs de la dernière heure
db.file_access_logs.find({
  "timestamp": {
    "$gte": new Date(Date.now() - 60*60*1000)
  }
})

# Compter les fichiers par catégorie
db.file_metadata.aggregate([
  {"$group": {
    "_id": "$category", 
    "count": {"$sum": 1}
  }}
}])

# Voir les fichiers les plus volumineux
db.file_metadata.find().sort({"file_size": -1}).limit(10)

📱 INTERFACE WEB SIMULTANÉMENT :
Pendant que vous explorez dans VS Code :
• Accédez à : http://localhost:8000/files/
• Connectez-vous avec admin/admin123
• Uploadez des fichiers
• Les changements apparaîtront en temps réel dans VS Code !

⚡ ASTUCES PRO :
1. Actualisation automatique : VS Code rafraîchit automatiquement
2. Requêtes favorites : Sauvegardez vos requêtes récurrentes
3. Export : Cliquez droit sur une collection → Export JSON
4. Index visualization : Voir les indexes créés pour optimisation

🎯 WORKFLOW OPTIMAL :
1. Uploadez un fichier via l'interface web (http://localhost:8000/files/)
2. Vérifiez immédiatement dans VS Code
3. Consultez les logs pour voir l'activité
4. Utilisez l'extension pour analyser les données

Votre base de données est maintenant accessible à la fois via :
✅ Interface web (Django) : http://localhost:8000/files/
✅ VS Code (MongoDB Extension) : Configuration ci-dessus
✅ Commandes Python : explore_mongodb.py