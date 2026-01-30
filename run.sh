#!/bin/bash

echo "========================================="
echo "ENISE Site - Starting Application"
echo "========================================="

# Set environment variables for HF Spaces
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=enise_site.settings

# Create migrations if they don't exist
echo "[1/6] Creating migrations..."
python manage.py makemigrations --no-input || true

# Run migrations (CRITICAL - DO NOT SUPPRESS OUTPUT)
echo "[2/6] Running database migrations..."
python manage.py migrate --noinput --verbosity 2 || {
    echo "ERROR: Migrations failed! Attempting again..."
    python manage.py migrate --noinput --verbosity 2
}

# Setup Appwrite collections
echo "[3/6] Setting up Appwrite collections..."
python manage.py setup_appwrite_collections || {
    echo "WARNING: Appwrite collection setup encountered issues"
}

# Seed Appwrite data
echo "[4/6] Seeding initial data to Appwrite..."
python manage.py seed_appwrite || {
    echo "WARNING: Appwrite data seeding encountered issues"
}

# Collect static files
echo "[5/6] Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2 || {
    echo "WARNING: Static file collection encountered issues"
}

# Start the server
echo "[6/6] Starting server on 0.0.0.0:7860..."
exec gunicorn enise_site.wsgi \
    --bind 0.0.0.0:7860 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
