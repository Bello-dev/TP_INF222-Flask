FROM python:3.9-slim

# Installer les dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt d'abord (pour le cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . /app

# Exposer le port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=run.py
ENV PYTHONPATH=/app

# Commande par défaut
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]