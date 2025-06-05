FROM python:3.11-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-traditional \
    curl \
    postgresql-client \
    iputils-ping \
    dnsutils \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /app

# Exposer le port 5000
EXPOSE 5000

# Définir les variables d'environnement
ENV FLASK_APP=run.py
ENV PYTHONPATH=/app

# Commande par défaut (remplacée par `command:` dans docker-compose.yml)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
