# Quick Reference: Appwrite Integration

## File Structure
```
enise_site/
├── appwrite_db.py               # ← Appwrite wrapper singleton
├── settings.py                  # ← Has APPWRITE_* env vars
└── wsgi.py

app_core/
├── services.py                  # ← 5 service classes (NEW)
├── views.py                     # ← Updated to use services (MODIFIED)
├── urls.py
├── models.py                    # ← Still exists but not used
└── management/commands/
    ├── setup_appwrite_collections.py  # ← Create schema (NEW)
    └── seed_appwrite.py               # ← Seed data (NEW)

templates/
├── app_core/
│   ├── index.html
│   ├── formations.html
│   └── specialite_detail.html

run.sh                           # ← 6-stage startup (MODIFIED)
test_appwrite_crud.py            # ← Test suite (NEW)
```

## How Data Flows

### Reading Data
```python
# In views.py
service = SpecialiteService()
specialites = service.list_all()  # → Appwrite API call → Cloud DB
```

### Service Layer Architecture
```python
# app_core/services.py
SpecialiteService
  ├── list_all()         # Query with sorting
  ├── get_by_slug()      # Query with filter
  ├── get_by_id()        # Direct document fetch
  ├── create()           # Insert new document
  ├── update()           # Modify existing
  └── delete()           # Remove document

ActualiteService, ContactService, PartenairesService, StatistiqueService
  └── (Similar pattern with collection-specific logic)
```

### Appwrite Wrapper Usage
```python
# enise_site/appwrite_db.py
db = get_appwrite_db()  # Singleton instance
db.list_documents('specialites', queries=[Query.order_asc('ordre')])
db.create_document('contact', data)
db.update_document('specialites', doc_id, updated_data)
db.delete_document('contact', doc_id)
```

## Collections Schema

### specialites
- nom: String(100) ✓
- slug: String(100) ✓
- description: String(65535) ✓
- image_url: URL
- icone: String(50)
- ordre: Integer

### actualites
- titre: String(200) ✓
- slug: String(200) ✓
- contenu: String(65535) ✓
- image_url: URL
- date_publication: DateTime ✓
- est_publie: Boolean ✓

### contact
- nom: String(100) ✓
- email: Email ✓
- sujet: String(200) ✓
- message: String(65535) ✓
- date_envoi: DateTime ✓
- traite: Boolean ✓

### partenaires
- nom: String(150) ✓
- logo_url: URL ✓
- url: URL
- type_partenaire: String(50) ✓

### statistiques
- nom: String(100) ✓
- valeur: String(50) ✓
- suffixe: String(10)
- icone: String(50) ✓
- ordre: Integer ✓

## Initial Data

### Specialites (3)
1. Génie Civil - génie-civil
2. Mécanique - mecanique
3. Physique - physique

### Actualites (3)
1. Bienvenue à l'ENISE - bienvenue-a-lenise
2. Événement scientifique 2024 - evenement-scientifique-2024
3. Internships et stages - internships-et-stages

### Statistiques (3)
1. Étudiants: 1200+
2. Années d'existence: 50+
3. Entreprises partenaires: 300+

### Partenaires (3)
1. SNCF - INDUSTRIEL
2. Université de Lyon - ACADEMIQUE
3. Région Auvergne-Rhône-Alpes - INSTITUTIONNEL

## Environment Variables Required

```bash
# Appwrite Cloud Configuration
APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=697abaca00272dab718b
APPWRITE_API_KEY=<your-api-key>
APPWRITE_DATABASE_ID=697cd79900149b10540c

# Django Settings
DEBUG=False
SECRET_KEY=<generated>
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=https://ktongue-enise.hf.space
```

## Testing Locally

```bash
# Run all tests
python test_appwrite_crud.py

# Run specific service tests
python manage.py shell
>>> from app_core.services import SpecialiteService
>>> service = SpecialiteService()
>>> specialites = service.list_all()
>>> len(specialites)
3

# Run management commands
python manage.py setup_appwrite_collections
python manage.py seed_appwrite

# Test views
python manage.py runserver
# Visit http://localhost:8000/
```

## Production Deployment

```bash
# run.sh automatically:
1. Creates migrations
2. Runs migrations
3. Calls setup_appwrite_collections
4. Calls seed_appwrite
5. Collects static files
6. Starts Gunicorn

# On HF Spaces, restart the space to trigger deployment
```

## Debugging

### Check Appwrite Connection
```python
from enise_site.appwrite_db import get_appwrite_db
db = get_appwrite_db()
db.test_connection()  # Returns True/False
```

### List Documents
```python
from app_core.services import SpecialiteService
service = SpecialiteService()
docs = service.list_all()
for doc in docs:
    print(doc)
```

### Check Logs
```bash
# Local development
# Check console output for ✅/❌ messages

# HF Spaces
# Check the "Logs" tab in HF Spaces interface
```

## Common Issues

### Collections already exist
- This is expected and handled gracefully
- The system skips creation and uses existing collections

### Data not seeding
- Check Appwrite API key in environment variables
- Check database ID is correct
- Verify collections were created successfully

### 404 on specialite detail
- Verify slug format matches: /specialite/slug-name/
- Check specialite exists in Appwrite by listing all
- Verify slug field is populated correctly

## Next Steps

1. ✅ Appwrite integration complete
2. ✅ All CRUD operations working
3. ✅ Data persistence implemented
4. ⏳ Optional: Debug frontend CSS issues
5. ⏳ Optional: Migrate admin panel to Appwrite queries

## Resources

- Appwrite Console: https://console.appwrite.io
- GitHub Repo: https://github.com/tiffank1802/enise-site-2
- HF Space: https://huggingface.co/spaces/ktongue/ENISE
- Documentation: See APPWRITE_INTEGRATION.md
