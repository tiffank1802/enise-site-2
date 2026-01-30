#!/bin/bash
set -e

echo "========================================="
echo "ENISE Site - Starting Application"
echo "========================================="

# Set environment variables for HF Spaces
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=enise_site.settings

# Collect static files
echo "[1/3] Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || echo "Static files already collected or skipped"

# Run migrations
echo "[2/3] Running database migrations..."
python manage.py migrate --noinput 2>/dev/null || echo "Migrations completed or no migrations needed"

# Start the server
echo "[3/3] Starting server on 0.0.0.0:7860..."
exec gunicorn enise_site.wsgi \
    --bind 0.0.0.0:7860 \
    --workers 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
