# Utilisation d'une image officielle de Python
FROM python:3.9

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY app app
COPY run.py run.py

# Installation des dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exposer le port de l'API Flask
EXPOSE 5000

# Définition de la commande de lancement
CMD ["python", "run.py"]
