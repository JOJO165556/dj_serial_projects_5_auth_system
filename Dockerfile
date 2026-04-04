# Utilise une image légère et performante
FROM python:3.12-slim

# Configuration pour Docker :
# Ne pas créer de fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Afficher directement les logs dans le terminal sans délai
ENV PYTHONUNBUFFERED=1

# Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Installer des petits utilitaires système si besoin
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . /app/
