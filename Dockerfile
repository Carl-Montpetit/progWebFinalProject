FROM python:3.9-slim-buster

# Créer le répertoire + ce déplacer dans le répertoire
# mkdir -p /app && cd /app
WORKDIR /app

# Configurer des variables d'environnement
ENV FLASK_APP=./app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copier ficher host -> image
COPY requirements.txt requirements.txt

# RUN = lancer une commande
RUN pip install -r requirements.txt

# Exposer port 8000 pour serveur web de flask
EXPOSE 5000

# Copier tous les fichiers du répertoire courant du host vers répertoire courant du l'image
COPY . .

CMD [ "flask", "run", "--host=0.0.0.0"]