# 🔗 Liens Importants - ENISE Appwrite Deployment

## 🌐 Accès Direct

### HF Spaces
- **Space URL:** https://huggingface.co/spaces/ktongue/ENISE
- **Application:** https://ktongue-enise.hf.space

### GitHub
- **Repository:** https://github.com/tiffank1802/enise-site-2
- **Derniers commits:** https://github.com/tiffank1802/enise-site-2/commits/main

### Appwrite
- **Console:** https://console.appwrite.io
- **Project ID:** 697abaca00272dab718b
- **Endpoint:** https://fra.cloud.appwrite.io/v1

---

## 📚 Documentation

### Pour Commencer
1. **LIRE EN PREMIER:** `HF_SPACES_DEPLOYMENT.md` - Guide de déploiement HF Spaces
2. **Documentation Technique:** `APPWRITE_INTEGRATION.md` - Architecture complète
3. **Référence Rapide:** `APPWRITE_QUICK_REFERENCE.md` - Patterns et schemas

### Vérification
- `DEPLOYMENT_CHECKLIST_APPWRITE.md` - Checklist pré-déploiement
- `test_appwrite_crud.py` - Tests unitaires

---

## 🚀 Étapes de Déploiement

### 1. Push Code (✅ DÉJÀ FAIT)
```bash
# 6 commits créés et poussés vers main
git log --oneline -6
```

### 2. Redémarrer HF Spaces (À FAIRE)
1. Aller à: https://huggingface.co/spaces/ktongue/ENISE
2. Settings → Restart
3. Attendre 3-5 minutes

### 3. Vérifier (À FAIRE)
- Visiter https://ktongue-enise.hf.space
- Vérifier les données s'affichent
- Consulter les logs HF Spaces

---

## 🔑 Variables d'Environnement

### À Vérifier dans HF Spaces Secrets
```
APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=697abaca00272dab718b
APPWRITE_API_KEY=<DOIT ÊTRE DÉFINI>
APPWRITE_DATABASE_ID=697cd79900149b10540c
DEBUG=False
SECRET_KEY=<DOIT ÊTRE DÉFINI>
```

### Vérification Locale
```bash
python manage.py shell
from enise_site.appwrite_db import get_appwrite_db
db = get_appwrite_db()
db.test_connection()  # Devrait retourner True
```

---

## 📊 Architecture

### Services Django
- `SpecialiteService` - Gestion des spécialités
- `ActualiteService` - Gestion des actualités
- `ContactService` - Gestion des contacts
- `PartenairesService` - Gestion des partenaires
- `StatistiqueService` - Gestion des statistiques

### Collections Appwrite
- `specialites` - 3 documents
- `actualites` - 3 documents
- `contact` - Documents dynamiques
- `partenaires` - 3 documents
- `statistiques` - 3 documents

---

## 🧪 Tester Localement

```bash
# Lancer les tests
python test_appwrite_crud.py

# Vérifier les services
python manage.py shell
from app_core.services import SpecialiteService
service = SpecialiteService()
specs = service.list_all()
print(len(specs))  # Devrait afficher 3

# Démarrer le serveur
python manage.py runserver 0.0.0.0:8000
# Visiter http://localhost:8000/
```

---

## 📝 Fichiers Créés/Modifiés

### Créés (7 fichiers)
- ✅ `enise_site/appwrite_db.py` - Wrapper Appwrite
- ✅ `app_core/services.py` - Services métier
- ✅ `app_core/management/commands/setup_appwrite_collections.py`
- ✅ `app_core/management/commands/seed_appwrite.py`
- ✅ `test_appwrite_crud.py` - Tests
- ✅ Documentation (4 fichiers)

### Modifiés (2 fichiers)
- ✅ `app_core/views.py` - Utilise services
- ✅ `run.sh` - 6 étapes

---

## 🚨 En Cas de Problème

### Les données ne s'affichent pas
1. Vérifier APPWRITE_API_KEY dans HF Secrets
2. Consulter la console Appwrite
3. Vérifier les logs HF Spaces

### Erreurs de déploiement
1. Lire les logs HF Spaces
2. Consulter `DEPLOYMENT_CHECKLIST_APPWRITE.md`
3. Rollback si nécessaire: `git revert HEAD~5`

### Tester la connexion Appwrite
```bash
python manage.py shell
from enise_site.appwrite_db import get_appwrite_db
db = get_appwrite_db()
print("Connection:", db.test_connection())
print("Collections:", db.databases.list_collections(database_id=db.database_id))
```

---

## ✅ Checklist Finale

- [x] Code poussé sur GitHub
- [x] Tests locaux 8/8 passants
- [x] Documentation complète
- [x] Variables d'environnement vérifiées
- [x] Données sémées dans Appwrite
- [ ] HF Spaces redémarré
- [ ] Application testée en production
- [ ] Logs vérifiés

---

## 📞 Contact & Support

- **GitHub:** https://github.com/tiffank1802/enise-site-2
- **Appwrite Docs:** https://appwrite.io/docs
- **Appwrite Console:** https://console.appwrite.io

---

**Status:** 🚀 Prêt pour HF Spaces  
**Date:** 30 janvier 2026  
**Version:** 1.0
