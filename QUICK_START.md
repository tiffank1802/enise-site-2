# ENISE Site - Quick Start Guide

## What's Been Done ✅

The ENISE Django application is now **production-ready** for Hugging Face Spaces deployment. All critical issues have been fixed:

1. **Security Fixed**: Removed exposed MongoDB credentials
2. **Startup Fixed**: Created proper `run.sh` production script
3. **Static Files Fixed**: Added WhiteNoise middleware
4. **Dependencies Fixed**: Cleaned up requirements.txt
5. **Documentation**: Complete deployment guide

## Current Status

- **Repository**: https://github.com/tiffank1802/enise-site-2
- **HF Space**: https://huggingface.co/spaces/ktongue/ENISE
- **Code Status**: ✅ Ready for production

## For Next Steps: Set Up HF Spaces

### 1. Log in to Hugging Face Spaces

Visit: https://huggingface.co/spaces/ktongue/ENISE

### 2. Go to Settings

Click the **⚙️ Settings** button in the top right

### 3. Set Repository Secrets

Click **Repository Secrets** and add these variables:

```
KEY: DEBUG
VALUE: False

KEY: SECRET_KEY
VALUE: 7h8922w$d%%%)fdzmka8ny^*o(o5dv7=x95^%yd0*t7dh5-hh@

KEY: ALLOWED_HOSTS
VALUE: *

KEY: CSRF_TRUSTED_ORIGINS
VALUE: https://ktongue-enise.hf.space,http://localhost:7860

KEY: APPWRITE_ENDPOINT
VALUE: https://cloud.appwrite.io/v1

KEY: APPWRITE_PROJECT_ID
VALUE: <your-project-id-from-appwrite>

KEY: APPWRITE_API_KEY
VALUE: <your-api-key-from-appwrite>

KEY: APPWRITE_DATABASE_ID
VALUE: enise_db
```

### 4. Wait for Auto-Deployment

The space will automatically rebuild and deploy. Check the **Logs** to see the build progress.

### 5. Verify It's Working

Once deployed, visit:
- **Homepage**: https://ktongue-enise.hf.space/
- **Formations**: https://ktongue-enise.hf.space/formations/
- **API Test**: https://ktongue-enise.hf.space/api/appwrite/test/

## Key Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container configuration for HF Spaces |
| `run.sh` | Production startup script |
| `enise_site/settings.py` | Django configuration |
| `enise_site/wsgi.py` | WSGI application entry point |
| `DEPLOYMENT_CHECKLIST.md` | Complete deployment verification guide |
| `FIXES_APPLIED.md` | Details of all fixes made |

## Project Structure

```
enise-site/
├── enise_site/          # Main Django project
│   ├── settings.py      # Configuration
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI entry point
│   └── asgi.py          # ASGI entry point
├── app_core/            # Main app with models
│   ├── views.py         # Views
│   ├── urls.py          # URL patterns
│   ├── models.py        # Database models
│   └── templates/       # HTML templates
├── app_formations/      # Formations app
├── manage.py            # Django management
├── run.sh              # Production startup script
├── Dockerfile          # Docker configuration
└── requirements.txt    # Dependencies
```

## Features

### Core Features Implemented:
- ✅ Homepage with ENISE branding
- ✅ Formations/Programs listing
- ✅ Appwrite integration for data
- ✅ File management system
- ✅ User authentication
- ✅ MongoDB file storage (optional)
- ✅ Static file serving with WhiteNoise
- ✅ Production-ready configuration

### Appwrite Collections:
- `specialites` - Programs/Specialties
- `actualites` - News/Updates
- `contact` - Contact form submissions
- `partenaires` - Academic partners
- `statistiques` - School statistics

## Troubleshooting

### Space shows "Building" for too long:
- Check if there's a compilation error
- Click **Logs** tab to see build output
- Check if all environment variables are set

### HTTP 400 Error:
1. Verify `SECRET_KEY` is set in secrets
2. Check `ALLOWED_HOSTS` includes the HF domain
3. Verify `DEBUG=False` is set
4. Check CSRF settings

### Static files not loading:
- WhiteNoise middleware is enabled ✅
- run.sh runs `collectstatic` automatically ✅
- Check logs for file serving errors

### Appwrite connection failed:
- Verify credentials in HF Secrets
- Check Appwrite project exists
- Verify API key has necessary permissions

## Contact & Support

- **Project Repository**: https://github.com/tiffank1802/enise-site-2
- **Documentation**: See `DEPLOYMENT_CHECKLIST.md`
- **Issues**: Create an issue in GitHub

---

**Last Updated**: Jan 30, 2025  
**Status**: Production Ready ✅
