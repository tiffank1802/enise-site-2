# ENISE Site - Production Deployment Guide

## 📋 Sommaire

Ce repository contient l'application ENISE Site - une plateforme web Django pour l'école d'ingénieurs ENISE, déployée sur Hugging Face Spaces avec intégration Appwrite.

- **Repository**: https://github.com/tiffank1802/enise-site-2
- **HF Space**: https://huggingface.co/spaces/ktongue/ENISE
- **Framework**: Django 5.0
- **Backend**: Appwrite Cloud
- **Deployment**: Docker sur HF Spaces

## ✨ Caractéristiques

### ✅ Implémentées
- Homepage avec branding ENISE
- Listing des formations/spécialisations
- Intégration Appwrite pour les données
- Système de gestion des fichiers
- Authentification utilisateur
- Stockage MongoDB (optionnel)
- Fichiers statiques avec WhiteNoise
- Configuration production-ready
- Documentation complète

### 🗄️ Collections Appwrite Disponibles
- `specialites` - Programs/Specialties
- `actualites` - News/Updates
- `contact` - Contact form submissions
- `partenaires` - Academic partners
- `statistiques` - School statistics

## 🚀 Déploiement Rapide

### 1️⃣ Configuration sur HF Spaces

1. Visitez: https://huggingface.co/spaces/ktongue/ENISE
2. Cliquez **⚙️ Settings**
3. Allez à **Repository Secrets**
4. Ajoutez ces variables (voir `QUICK_START.md` pour valeurs):

```
DEBUG=False
SECRET_KEY=<votre-clé>
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=https://ktongue-enise.hf.space
APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=<votre-id>
APPWRITE_API_KEY=<votre-clé> ⚠️
APPWRITE_DATABASE_ID=<votre-db-id>
```

### 2️⃣ Vérification

Une fois configuré, le space se redémarrera automatiquement.

Testez les endpoints:
- Homepage: https://ktongue-enise.hf.space/
- Formations: https://ktongue-enise.hf.space/formations/
- API: https://ktongue-enise.hf.space/api/appwrite/test/

Voir `VERIFIER_DEPLOIEMENT.md` pour guide complet.

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `QUICK_START.md` | Démarrage rapide |
| `DEPLOYMENT_CHECKLIST.md` | Checklist complète |
| `VERIFIER_DEPLOIEMENT.md` | Guide vérification (FR) |
| `DEPLOYMENT_STATUS.md` | État du déploiement |
| `FIXES_APPLIED.md` | Corrections appliquées |

## 🔧 Technologies

| Composant | Version |
|-----------|---------|
| Python | 3.11+ |
| Django | 5.0+ |
| Appwrite | 1.0+ |
| WhiteNoise | 6.5+ |
| PostgreSQL | optionnel |

## 📊 Structure du Projet

```
enise-site/
├── enise_site/                 # Django project
│   ├── settings.py             # Configuration
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI entry
├── app_core/                   # Main application
│   ├── models.py               # ORM models
│   ├── views.py                # Views
│   ├── urls.py                 # Routes
│   └── templates/              # HTML templates
├── app_formations/             # Formations app
├── static/                     # CSS, JS, images
├── media/                      # User uploads
├── Dockerfile                  # Docker config
├── run.sh                      # Startup script
├── requirements.txt            # Dependencies
└── manage.py                   # Django CLI
```

## 🔐 Configuration de Sécurité

### ✅ Appliquée
- Credentials MongoDB supprimées ✓
- SECRET_KEY en variables d'env ✓
- DEBUG=False en production ✓
- WhiteNoise pour fichiers statiques ✓
- CSRF protection configurée ✓
- API keys en HF Secrets ✓

### ⚠️ À Faire
- Jamais committer `.env`
- Régénérer SECRET_KEY pour chaque deployment
- Utiliser HTTPS en production
- Limiter ALLOWED_HOSTS si besoin

## 🧪 Tests

### Tests Locaux

```bash
# Vérifier configuration
python manage.py check

# Tester déploiement
python test_deployment.py

# Vérifier variables d'env
python check_env.py
```

### Tests HF Spaces

1. Vérifier status "Running"
2. Tester endpoints (voir `VERIFIER_DEPLOIEMENT.md`)
3. Vérifier logs en cas d'erreur

## 🚨 Dépannage

### Space "Building"
- C'est normal, attendez 5-10 minutes
- Vérifiez logs si > 15 min

### HTTP 400
- Vérifier `SECRET_KEY` configurée
- Vérifier `ALLOWED_HOSTS=*`
- Vérifier `DEBUG=False`

### API Appwrite échoue
- Vérifier `APPWRITE_API_KEY`
- Vérifier IDs du projet/database
- Régénérer clé si besoin

### Files statiques ne chargent pas
- WhiteNoise est activé ✓
- Vérifier `.log` pour erreurs
- Redémarrer le space

Voir `VERIFIER_DEPLOIEMENT.md` pour plus de solutions.

## 📈 Monitoring

Vérifiez régulièrement:

1. **Status du Space**: https://huggingface.co/spaces/ktongue/ENISE
2. **Logs**: Settings → Logs
3. **Endpoints**: Tester régulièrement
4. **Errors**: Chercher "ERROR" dans les logs

## 🔄 Mise à Jour

Pour déployer une mise à jour:

```bash
# 1. Faire changements localement
# 2. Tester localement
python manage.py check

# 3. Commit et push
git add .
git commit -m "Description"
git push origin main

# 4. HF Spaces redéploie automatiquement
# 5. Vérifier logs et endpoints
```

## 📞 Support

- **Issues**: https://github.com/tiffank1802/enise-site-2/issues
- **Docs**: Voir fichiers `*.md` dans le repo
- **Appwrite**: https://console.appwrite.io

## 📝 Notes Importantes

1. **Credentials**: Ne jamais committer secrets
2. **Branches**: Main = production, utilisez branches pour dev
3. **Migrations**: Auto-exécutées par `run.sh`
4. **Static Files**: Auto-collectés par `run.sh`
5. **Logs**: Disponibles dans HF Spaces Settings

## ✅ Dernière Vérification

Avant de considérer le déploiement comme "done":

- [ ] Space status = "Running"
- [ ] Pas d'erreurs dans les logs
- [ ] Homepage charge (200 OK)
- [ ] Formations visibles
- [ ] API test répond
- [ ] Static files chargent
- [ ] Admin panel accessible
- [ ] Appwrite connecté (avec API Key)

## 📊 Status

- **Code**: ✅ Production-ready
- **Tests**: ✅ Tous passent
- **Documentation**: ✅ Complète
- **Deployment**: ✅ Prêt

**Dernière mise à jour**: Jan 30, 2025

---

Pour commencer, consultez `QUICK_START.md` ou `VERIFIER_DEPLOIEMENT.md`.
