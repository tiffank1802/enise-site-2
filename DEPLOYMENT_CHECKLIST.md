# HF Spaces Deployment Checklist

## Pre-Deployment Verification ✅

**Local Setup Verification:**
- ✅ Django configuration valid (`python manage.py check`)
- ✅ All migrations planned and ready
- ✅ No hardcoded secrets in code
- ✅ WhiteNoise middleware configured for static files
- ✅ GitHub repository synced with latest changes
- ✅ run.sh script created and executable

## HF Spaces Configuration Required

### 1. Set Environment Variables (Critical)

Go to: **HuggingFace Space Settings → Repository Secrets**

**Copy and paste each line as a separate secret:**

```
DEBUG=False
SECRET_KEY=django-insecure-abc123def456ghi789jkl012mno345pqr67890stu12345
ALLOWED_HOSTS=*
CSRF_TRUSTED_ORIGINS=https://ktongue-enise.hf.space,http://localhost:7860
```

**For Appwrite Integration:**
```
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id-here
APPWRITE_API_KEY=your-api-key-here
APPWRITE_DATABASE_ID=enise_db
```

**For MongoDB (if needed):**
```
MONGO_DB_HOST=your-mongodb-host.mongodb.net
MONGO_DB_PORT=27017
MONGO_DB_USER=your-username
MONGO_DB_PASSWORD=your-password
MONGO_DB_NAME=enise_filesystem
```

### 2. Verify Space Settings

- **Title**: ENISE Site
- **Emoji**: 📚
- **Visibility**: Public (or Private)
- **License**: Apache 2.0 (or your choice)
- **Hardware**: CPU (sufficient for Django) or GPU (if ML needed)

### 3. Monitor Deployment

1. Push changes to GitHub: ✅ Done
2. Wait 30-60 seconds for HF to detect changes
3. Check Space Build Status:
   - Go to: https://huggingface.co/spaces/ktongue/ENISE
   - Click **⚙️ Settings → Logs**
   - Look for "Build started" and "Build completed"

### 4. Verify Application

Once deployed, test these endpoints:

**Home Page:**
```
https://ktongue-enise.hf.space/
```
Expected: ENISE homepage with formations list

**API Health Check:**
```
https://ktongue-enise.hf.space/api/appwrite/test/
```
Expected: JSON response indicating Appwrite connection status

**Static Files:**
```
https://ktongue-enise.hf.space/static/style.css
```
Expected: CSS file loads (200 OK)

### 5. Troubleshooting

**If you see HTTP 400 error:**
1. Check HF Logs for full error message
2. Verify all environment variables are set
3. Check SECRET_KEY is not empty
4. Ensure ALLOWED_HOSTS includes the HF domain

**If migrations fail:**
1. Check database is accessible
2. Verify DATABASE_ENGINE is set correctly
3. Check logs for specific migration errors

**If static files don't load:**
1. WhiteNoise middleware should be enabled ✅
2. Check STATIC_URL and STATIC_ROOT are configured ✅
3. Verify run.sh runs `collectstatic` ✅

**If Appwrite connection fails:**
1. Verify APPWRITE_PROJECT_ID is correct
2. Check APPWRITE_API_KEY is valid
3. Verify APPWRITE_ENDPOINT is accessible
4. Check APPWRITE_DATABASE_ID exists in Appwrite

## Deployment Success Indicators

- ✅ Space shows "Running" status
- ✅ Home page loads (/)
- ✅ Static files load (CSS, JS, images)
- ✅ No 400/500 errors in logs
- ✅ API endpoints respond with correct data
- ✅ Appwrite connection test passes

## Post-Deployment Steps

1. **Test Core Functionality:**
   - [ ] Homepage loads properly
   - [ ] Formations page works
   - [ ] File manager accessible (if logged in)
   - [ ] Appwrite CRUD operations work

2. **Monitor for Issues:**
   - [ ] Check Space logs regularly
   - [ ] Set up error notifications if possible
   - [ ] Monitor space uptime

3. **Update Documentation:**
   - [ ] Document any customizations made
   - [ ] Update README with live URL
   - [ ] Create deployment notes for team

## Quick Commands for Debugging

**SSH into the running space (if enabled):**
```bash
# View logs in real-time
docker logs -f [container-id]

# Check migrations
python manage.py showmigrations

# Test Django setup
python manage.py shell
# In shell:
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
>>> print(settings.APPWRITE_PROJECT_ID)
```

## Important Notes

- **Never commit `.env` files** - always use HF Secrets
- **Regenerate SECRET_KEY for production** - use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **Monitor resource usage** - adjust workers/threads if needed
- **Keep dependencies updated** - run `pip freeze > requirements.txt` after updates

---

**Deployment Status**: Ready for production ✅
**Last Updated**: Jan 30, 2025
**Repository**: https://github.com/tiffank1802/enise-site-2
**HF Space**: https://huggingface.co/spaces/ktongue/ENISE
