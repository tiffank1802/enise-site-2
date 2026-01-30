# Configuration Appwrite pour Django ENISE Site

## Prérequis

1. **Compte Appwrite Cloud** ou serveur Appwrite auto-hébergé
2. **Python 3.9+**
3. **Django 4.2+**

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=enise_db
```

### 2. Créer le projet Appwrite

1. Connectez-vous à [Appwrite Cloud](https://cloud.appwrite.io)
2. Créez un nouveau projet : `enise-site`
3. Notez l'**ID du projet**
4. Créez une base de données : `enise_db`

### 3. Créer les collections

Dans le tableau de bord Appwrite, créez ces collections :

| Collection | Attributs |
|------------|-----------|
| **specialites** | nom (string), slug (string), description (string), image_url (url), icone (string), ordre (integer) |
| **actualites** | titre (string), slug (string), contenu (string), image_url (url), date_publication (datetime), est_publie (boolean) |
| **contact** | nom (string), email (email), sujet (string), message (string), date_envoi (datetime), traite (boolean) |
| **partenaires** | nom (string), logo_url (url), url (url), type_partenaire (string) |
| **statistiques** | nom (string), valeur (string), suffixe (string), icone (string), ordre (integer) |

### 4. Configurer les permissions

Pour chaque collection, configurez les permissions :
- **create**: Rôle `any` (ou utilisateur connecté)
- **read**: Rôle `any`
- **update**: Rôle `any`
- **delete**: Rôle `admin`

## Commandes Django

### Créer les collections automatiquement

```bash
python manage.py setup_appwrite
```

### Tester la connexion

```bash
python manage.py sync_appwrite --test
```

### Synchroniser les données locales vers Appwrite

```bash
python manage.py sync_appwrite
```

## API REST Endpoints

Les vues Appwrite sont disponibles à ces URLs :

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/appwrite/test/` | Tester la connexion |
| POST | `/api/appwrite/documents/` | Créer un document |
| GET | `/api/appwrite/documents/` | Lister les documents |
| GET | `/api/appwrite/documents/<id>/` | Récupérer un document |
| PUT | `/api/appwrite/documents/<id>/` | Mettre à jour un document |
| DELETE | `/api/appwrite/documents/<id>/` | Supprimer un document |

### Exemple d'utilisation

**Créer un document :**
```bash
curl -X POST http://localhost:8000/api/appwrite/documents/ \
  -H "Content-Type: application/json" \
  -d '{
    "collection_id": "specialites",
    "nom": "Génie Civil",
    "slug": "genie-civil",
    "description": "Formation en génie civil",
    "icone": "fa-building",
    "ordre": 1
  }'
```

**Lister les documents :**
```bash
curl "http://localhost:8000/api/appwrite/documents/?collection_id=specialites"
```

## Structure des fichiers

```
enise_site/
├── settings.py              # Configuration Django
├── appwrite_service.py      # Client Appwrite
app_core/
├── appwrite_views.py        # Vues API REST
├── management/commands/
│   ├── setup_appwrite.py    # Créer les collections
│   └── sync_appwrite.py     # Synchroniser les données
requirements.txt
.env.example
```

## Déploiement sur Hugging Face Spaces

1. Créez un fichier `Procfile` :
   ```
   web: gunicorn enise_site.wsgi
   ```

2. Configurez les variables d'environnement dans HF Spaces

3. Poussez le projet :
   ```bash
   git add .
   git commit -m "Appwrite integration"
   git push
   ```

## Documentation

- [SDK Python Appwrite](https://appwrite.io/docs/sdk-for-python)
- [API Database](https://appwrite.io/docs/databases)
- [Appwrite Cloud](https://cloud.appwrite.io)

## Résolution des problèmes

- **"APPWRITE_PROJECT_ID non configuré"** : Vérifiez le fichier `.env`
- **Erreur 401** : Vérifiez la clé API
- **Erreur 404** : Vérifiez l'ID de la collection