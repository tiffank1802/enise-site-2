# Guide de Vérification du Déploiement - ENISE Site

## 🎯 Vue d'ensemble

Le code de l'ENISE Site est maintenant **prêt pour la production** sur Hugging Face Spaces.

**Status**: ✅ Tous les tests locaux passent

## ✅ Étapes de Vérification

### Étape 1: Vérifier le Status du Space

1. Allez sur: https://huggingface.co/spaces/ktongue/ENISE
2. Vérifiez le statut en haut à droite
3. **Acceptable**: ✅ "Running"
4. **À attendre**: ⏳ "Building" (relancer après quelques minutes)
5. **Problème**: ❌ "Error" (vérifier les logs)

### Étape 2: Vérifier les Logs

Si le status est "Building" ou "Error":

1. Cliquez sur **⚙️ Settings** (engrenage en haut à droite)
2. Cliquez sur l'onglet **Logs**
3. Vous devriez voir ceci (scroll si besoin):

```
# Logs attendus (ordre chronologique):

1. "Starting build..."
2. "Building Docker image..."
3. "docker run ... ./run.sh"
4. "[INFO] Collecting static files..."
5. "[INFO] Running database migrations..."
6. "[INFO] Starting server on 0.0.0.0:7860..."
```

**Si vous voyez une erreur**, notez le message exact.

### Étape 3: Tester les Endpoints

Une fois le status "Running", testez ces URLs:

#### 3.1 Homepage (Test Principal)
```
https://ktongue-enise.hf.space/
```

**Expected**: 
- ✅ Page web s'affiche
- ✅ Titre: "ENISE" visible
- ✅ Formations listées
- ✅ Pas d'erreur 500

**Si erreur**:
- Vérifier que les static files chargent (CSS, images)
- Consulter les logs

#### 3.2 Page Formations
```
https://ktongue-enise.hf.space/formations/
```

**Expected**: 
- ✅ Liste des formations s'affiche
- ✅ Status 200

#### 3.3 Test Appwrite (Important!)
```
https://ktongue-enise.hf.space/api/appwrite/test/
```

**Expected**: Réponse JSON comme:
```json
{
  "status": "ok",
  "message": "Appwrite connection successful",
  "project_id": "697abaca00272dab718b",
  "database_id": "697cd79900149b10540c"
}
```

**ou** si API Key manquante:
```json
{
  "status": "error",
  "message": "Authentication failed",
  "error": "Invalid API key"
}
```

> Si vous voyez une erreur d'authentification Appwrite, cela signifie que `APPWRITE_API_KEY` n'est pas bien configurée dans HF Secrets.

#### 3.4 Admin Panel
```
https://ktongue-enise.hf.space/admin/
```

**Expected**: 
- ✅ Page de login Django
- ✅ Vous pouvez vous identifier
- ✅ Pas d'erreur 500

### Étape 4: Vérifier les Fichiers Statiques

Dans la page d'accueil, ouvrez les DevTools (F12) et:

1. Allez à l'onglet **Network**
2. Rechargez la page (F5)
3. Regardez les fichiers chargés

**À vérifier**:
- ✅ `style.css` → Status **200** (pas 404)
- ✅ Images → Status **200** (pas 404)
- ✅ Pas d'erreur en console rouge

Si vous voyez des erreurs 404 sur les fichiers statiques:
- Les fichiers ne sont pas servis correctement
- Vérifier que WhiteNoise est activé (il l'est ✅)

### Étape 5: Vérifier les Variables d'Environnement

Si quelque chose ne fonctionne pas, vérifiez les secrets HF:

1. Allez sur https://huggingface.co/spaces/ktongue/ENISE
2. Cliquez **⚙️ Settings**
3. Cliquez **Repository secrets**
4. Vérifiez que ces variables existent:

```
✓ DEBUG (value: False)
✓ SECRET_KEY (value: caché)
✓ ALLOWED_HOSTS (value: *)
✓ CSRF_TRUSTED_ORIGINS (value: https://ktongue-enise.hf.space,...)
✓ APPWRITE_ENDPOINT (value: https://fra.cloud.appwrite.io/v1)
✓ APPWRITE_PROJECT_ID (value: 697abaca00272dab718b)
✓ APPWRITE_API_KEY (value: caché) ⚠️ IMPORTANT
✓ APPWRITE_DATABASE_ID (value: 697cd79900149b10540c)
```

**Si une variable manque**:
1. Cliquez "Add secret"
2. Remplissez la variable
3. Cliquez "Save"
4. Le space redémarrera automatiquement

## 🚨 Problèmes Courants et Solutions

### Problème 1: Status "Building" depuis longtemps

**Cause**: La construction du Docker est en cours

**Solution**:
1. Attendez 5-10 minutes
2. Vérifiez les logs
3. Si l'erreur persiste, regardez les logs pour plus de détails

### Problème 2: HTTP 400 ou 403

**Causes possibles**:
1. `SECRET_KEY` non configurée
2. `ALLOWED_HOSTS` incorrect
3. `CSRF_TRUSTED_ORIGINS` manquant

**Solution**:
1. Vérifiez les secrets dans HF Spaces
2. Assurez-vous que `ALLOWED_HOSTS=*`
3. Redémarrez le space (Settings → Restart)

### Problème 3: Static files ne chargent pas (styles cassés)

**Cause**: WhiteNoise ne sert pas les fichiers correctement

**Solution**:
1. Vérifiez dans les logs l'erreur
2. Assurez-vous que `run.sh` exécute `collectstatic`
3. Vérifiez que le Dockerfile utilise `./run.sh`

**Status**: ✅ WhiteNoise est configuré - ce problème ne devrait pas survenir

### Problème 4: Erreur "Authentication failed" sur /api/appwrite/test/

**Cause**: `APPWRITE_API_KEY` est invalide ou manquante

**Solution**:
1. Allez sur https://console.appwrite.io
2. Générez une nouvelle clé API
3. Mettez à jour `APPWRITE_API_KEY` dans HF Secrets
4. Redémarrez le space

### Problème 5: Page blanche ou erreur 500

**Causes possibles**:
1. Erreur dans Django
2. Base de données inaccessible
3. Configuration manquante

**Solution**:
1. Vérifiez les logs HF Spaces
2. Cherchez "ERROR" ou "EXCEPTION" dans les logs
3. Notez le message d'erreur exact
4. Vérifiez la configuration dans `enise_site/settings.py`

## ✨ Tests de Fonctionnalité

### Test 1: Homepage Charge Correctement

```bash
# Commande (à exécuter localement si vous avez accès):
curl -I https://ktongue-enise.hf.space/

# Expected:
# HTTP/1.1 200 OK
# Content-Type: text/html; charset=utf-8
```

### Test 2: API Fonctionne

```bash
curl -s https://ktongue-enise.hf.space/api/appwrite/test/ | python -m json.tool

# Expected: JSON response avec status "ok" ou "error"
```

### Test 3: Admin Accessible

```bash
curl -I https://ktongue-enise.hf.space/admin/

# Expected:
# HTTP/1.1 302 Found  (redirection vers login)
# ou
# HTTP/1.1 200 OK  (si déjà connecté)
```

## 📊 Résumé de Vérification

**Checklist pour confirmer le succès**:

- [ ] Space status = "Running"
- [ ] Pas d'erreurs dans les logs
- [ ] GET / → Page visible (200 OK)
- [ ] GET /formations/ → Fonctionne (200 OK)
- [ ] GET /api/appwrite/test/ → JSON response
- [ ] CSS et images chargent (DevTools Network)
- [ ] GET /admin/ → Page login ou 302 redirect
- [ ] Pas d'erreurs 400/500

**Si tous les éléments sont cochés**: ✅ **DÉPLOIEMENT RÉUSSI!**

## 🔧 Dépannage Avancé

Si vous avez toujours des problèmes:

### 1. Vérifier la Docker Image Localement

```bash
# Cloner le repo
git clone https://github.com/tiffank1802/enise-site-2.git
cd enise-site-2

# Construire l'image
docker build -t enise-test .

# Exécuter avec variables d'env
docker run -p 7860:7860 \
  -e DEBUG=False \
  -e SECRET_KEY=test-key \
  -e ALLOWED_HOSTS=* \
  -e APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1 \
  -e APPWRITE_PROJECT_ID=your-id \
  -e APPWRITE_API_KEY=your-key \
  -e APPWRITE_DATABASE_ID=your-db-id \
  enise-test

# Visiter http://localhost:7860
```

### 2. Vérifier les Logs en Direct

Sur HF Spaces → Settings → Logs:
- Cherchez "ERROR"
- Cherchez "EXCEPTION"
- Cherchez "FAILED"

Copiez le message d'erreur complet pour diagnostic.

### 3. Redémarrer le Space

1. Allez sur le Space
2. Settings → Environment
3. Cliquez "Restart"

Cela redémarrera le container et rechargera les variables d'environnement.

## 📚 Ressources

- **GitHub Repo**: https://github.com/tiffank1802/enise-site-2
- **HF Space**: https://huggingface.co/spaces/ktongue/ENISE
- **Documentation**:
  - `QUICK_START.md` - Configuration rapide
  - `DEPLOYMENT_CHECKLIST.md` - Checklist complète
  - `FIXES_APPLIED.md` - Détails techniques

---

**Dernière mise à jour**: Jan 30, 2025  
**Status**: ✅ Code production-ready  
**Prochaine étape**: Tester le space et confirmer le fonctionnement
