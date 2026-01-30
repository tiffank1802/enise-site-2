FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p staticfiles media logs

# Exposer le port
EXPOSE 7860

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Commande de démarrage
CMD ["gunicorn", "enise_site.wsgi", "--bind", "0.0.0.0:7860", "--workers", "2"]