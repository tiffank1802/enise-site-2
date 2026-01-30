# Guide de déploiement sur Hugging Face Spaces

## Configuration pour la production

Ce guide explique comment déployer le projet Django ENISE Site sur Hugging Face Spaces avec Appwrite.

## Architecture

```
Hugging Face Spaces (Frontend + Django API)
    ↓
Appwrite Cloud (Backend + Base de données)
```

## Prérequis

- Compte [Hugging Face](https://huggingface.co)
- Projet et credentials [Appwrite Cloud](https://cloud.appwrite.io)
- Variables d'environnement configurées

## Déploiement sur Hugging Face Spaces

### 1. Créer un nouvel espace

1. Aller sur [huggingface.co/spaces](https://huggingface.co/spaces)
2. Cliquer sur "Create new Space"
3. Remplir les informations :
   - **Owner** : Ton compte
   - **Space name** : `enise-site` (ou autre)
   - **License** : MIT (recommandé)
   - **Space SDK** : Docker
   - **Visibility** : Public

### 2. Configurer les variables d'environnement

Dans les **Space settings** (roue dentée en haut) :

**Variables secrètes :**
```
APPWRITE_ENDPOINT = https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID = ton_project_id
APPWRITE_API_KEY = ta_cle_api
APPWRITE_DATABASE_ID = enise_db
SECRET_KEY = une_clé_secrète_très_forte
ALLOWED_HOSTS = enise-site.hf.space,*.hf.space
DEBUG = False
```

### 3. Pousser le code

```bash
# Clone le dépôt HF
git clone https://huggingface.co/spaces/ton-username/enise-site
cd enise-site

# Ajoute le remote de ton projet
git remote add origin https://github.com/tiffank1802/enise-site-2.git
git pull origin main

# Configure ton user HF
git config user.email "ton_email@example.com"
git config user.name "ton_username"

# Push sur HF Spaces
git push -u origin main:main
```

Ou directement :
```bash
git clone https://github.com/tiffank1802/enise-site-2.git
cd enise-site-2
git remote add hf https://huggingface.co/spaces/ton-username/enise-site
git push hf main
```

## Structure des fichiers

| Fichier | Description |
|---------|------------|
| `Procfile` | Configuration Heroku (optionnel) |
| `Dockerfile` | Configuration Docker pour HF Spaces |
| `app.py` | Script de démarrage |
| `requirements.txt` | Dépendances Python |
| `enise_site/settings.py` | Configuration Django |
| `.env.example` | Template pour les variables |

## Commandes de maintenance

### Créer les migrations sur HF
```bash
# Depuis la console HF (dans le fichier app.py)
# Les migrations se font automatiquement au démarrage
```

### Créer les collections Appwrite
```bash
python manage.py setup_appwrite
```

### Synchroniser les données
```bash
python manage.py sync_appwrite
```

## Variables d'environnement

### Requises
- `APPWRITE_ENDPOINT` - URL d'Appwrite
- `APPWRITE_PROJECT_ID` - ID du projet
- `APPWRITE_API_KEY` - Clé API
- `APPWRITE_DATABASE_ID` - ID de la base de données

### Optionnelles
- `SECRET_KEY` - Clé secrète Django (générée automatiquement)
- `DEBUG` - Mode debug (False en production)
- `ALLOWED_HOSTS` - Domaines autorisés
- `DATABASE_ENGINE` - sqlite3 (défaut) ou postgresql
- `CSRF_TRUSTED_ORIGINS` - Origines CSRF autorisées
- `SECURE_SSL_REDIRECT` - Forcer HTTPS
- `SESSION_COOKIE_SECURE` - Cookies sécurisés

## Monitoring

### Logs sur HF Spaces
- Accède à l'onglet "Logs" dans les paramètres du Space
- Tu verras les logs de démarrage et d'erreurs

### Vérifier l'état
```bash
curl https://ton-space.hf.space/api/appwrite/test/
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'appwrite'"
→ Vérifier `requirements.txt` et redéployer

### "APPWRITE_PROJECT_ID not found"
→ Ajouter les variables dans les secrets du Space

### "Database connection refused"
→ Vérifier la configuration Appwrite et les identifiants

### "Static files not loading"
```bash
python manage.py collectstatic --noinput
```

## Optimisation pour production

### Performance
- Activer la compression GZIP
- Utiliser un CDN pour les fichiers statiques
- Configurer le cache HTTP

### Sécurité
- Définir `DEBUG = False`
- Activer `SECURE_SSL_REDIRECT = True`
- Utiliser des sessions sécurisées
- Mettre à jour régulièrement les dépendances

### Backup
- Exporter régulièrement les données Appwrite
- Garder une copie des migrations

## Support

- **Hugging Face Docs** : https://huggingface.co/docs/hub/spaces
- **Django Docs** : https://docs.djangoproject.com
- **Appwrite Docs** : https://appwrite.io/docs

## Licence

MIT License - Voir LICENSE pour plus de détails