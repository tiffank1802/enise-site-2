#!/bin/bash

echo "========================================="
echo "ENISE Site - Starting Application"
echo "========================================="

# Set environment variables for HF Spaces
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=enise_site.settings

# Create migrations if they don't exist
echo "[1/5] Creating migrations..."
python manage.py makemigrations --no-input || true

# Run migrations (CRITICAL - DO NOT SUPPRESS OUTPUT)
echo "[2/5] Running database migrations..."
python manage.py migrate --noinput --verbosity 2 || {
    echo "ERROR: Migrations failed! Attempting again..."
    python manage.py migrate --noinput --verbosity 2
}

# Load initial data
echo "[3/5] Loading initial data..."
python manage.py loaddata app_core/fixtures/initial_data.json --verbosity 2 || {
    echo "INFO: Initial data already loaded or file not found"
}

# Collect static files
echo "[4/5] Collecting static files..."
python manage.py collectstatic --noinput --verbosity 2 || {
    echo "WARNING: Static file collection encountered issues"
}

# Start the server
echo "[5/5] Starting server on 0.0.0.0:7860..."
exec gunicorn enise_site.wsgi \
    --bind 0.0.0.0:7860 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
