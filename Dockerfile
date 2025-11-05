# Utilise une image de base Python
FROM python:3.13-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app 

# Copier les fichiers du projet dans le conteneur
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Installler toutes les dépendances du projet
COPY . .
# # Installer les dépendances
# COPY pyproject.toml ./
# RUN pip install --upgrade pip && pip install .

# Ouvrir le port utilisé par FastAPI (8000 par défaut)
EXPOSE 8000

# Commande pour lancer l’API
CMD ["python", "API_fraude.main.py"]

# Pour lancer l'application, utilisez la commande suivante :
# podman build -t api-fraud:V0 .
# podman run -d -p 8000:8000 api-fraud:V0
# Pour accéder à l'API, ouvrez votre navigateur à l'adresse http://localhost:8000/docs
# Pour exécuter les tests, utilisez la commande suivante :
# podman run -p 8000:8000 api-fraud pytest
# podman ps -a : pour vérifier tous les conteneurs 
# podman ps : pour vérifier les conteneurs en cours d'exécution
# podman machine stop : pour arrêter la machine virtuelle
# podman machine start : pour démarrer la machine virtuelle