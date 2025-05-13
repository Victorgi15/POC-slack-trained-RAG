Projet Qdrant Docker
Ce projet configure un environnement Docker pour exécuter Qdrant, une base de données vectorielle de type "search engine". L'objectif est de mettre en place un service Qdrant en utilisant Docker Compose et de gérer l'environnement à l'aide d'un fichier .env pour les paramètres de configuration.

📋 Prérequis
Avant de commencer, vous devez avoir installé :

Docker : Téléchargez Docker

Docker Compose : Il est inclus avec Docker Desktop sur Windows.

🚀 Configuration

1. Clonez ce projet
   Si ce projet n'a pas encore été cloné, clonez-le depuis GitHub :

bash
Copier
Modifier
git clone https://github.com/Victorgi15/My_first-RAG.git
cd My_first-RAG 2. Configurer le fichier .env
Dans la racine de votre projet, créez un fichier .env pour stocker les variables d'environnement nécessaires à la configuration de Qdrant.

Voici un exemple de ce que pourrait contenir ton fichier .env :

env
Copier
Modifier
QDRANT_API_KEY=superclesecrete123
QDRANT_PORT=6333
Variables :

QDRANT_API_KEY : La clé API pour authentifier les requêtes vers Qdrant.

QDRANT_PORT : Le port sur lequel Qdrant sera accessible.

3. Configurer Docker Compose
   Dans ton projet, tu devrais avoir un fichier docker-compose.yml qui configure Qdrant avec Docker. Voici un exemple simple :

yaml
Copier
Modifier
version: '3.7'

services:
qdrant:
image: qdrant/qdrant:latest
environment: - SERVICE*FQDN_QDRANT*${QDRANT_PORT:-6333}
      - QDRANT__SERVICE__API_KEY=${QDRANT_API_KEY}
ports: - ${QDRANT_PORT:-6333}:${QDRANT_PORT:-6333}
volumes: - "qdrant_data:/qdrant/storage"
healthcheck:
test: - CMD-SHELL - bash -c ':> /dev/tcp/127.0.0.1/${QDRANT_PORT:-6333}' || exit 1
interval: 5s
timeout: 5s
retries: 3

networks:
backend-network:
driver: bridge

volumes:
qdrant_data: {}
Explication :

Ce fichier lance un container Docker pour Qdrant.

Il utilise les variables d'environnement définies dans le fichier .env.

Il mappe le port du container vers ton système pour que tu puisses y accéder.

Il configure également un volume pour persister les données de Qdrant.

4. Construire et démarrer les containers
   Une fois ton fichier docker-compose.yml et ton fichier .env configurés, tu peux construire et démarrer les containers avec Docker Compose :

bash
Copier
Modifier
docker-compose up -d
Cela démarrera le service Qdrant en arrière-plan.

5. Vérifier le service
   Tu peux vérifier que Qdrant fonctionne correctement en accédant à son API via le port configuré. Par défaut, cela sera accessible à http://localhost:6333.

Utilise la commande suivante pour tester la connexion au service :

bash
Copier
Modifier
curl http://localhost:6333
Tu devrais obtenir une réponse de Qdrant, confirmant qu'il fonctionne.

📝 Git et gestion de versions
Initialisation du dépôt Git
Initialiser le dépôt Git localement :

bash
Copier
Modifier
git init
Ajouter un fichier .gitignore pour ignorer les fichiers sensibles comme .env et les configurations spécifiques à l'IDE :

bash
Copier
Modifier
echo ".env" >> .gitignore
echo ".env.\*" >> .gitignore
echo ".vscode/" >> .gitignore
Faire un commit initial :

bash
Copier
Modifier
git add .
git commit -m "Initial commit with Docker and Qdrant setup"
Lier le dépôt local à GitHub
Crée un dépôt sur GitHub sans fichier README ni .gitignore.

Relie ton dépôt local à GitHub avec :

bash
Copier
Modifier
git remote add origin https://github.com/Victorgi15/My_first-RAG.git
git branch -M main
git push -u origin main
💡 Ressources utiles
Qdrant Documentation

Docker Documentation

GitHub Documentation

🎯 Conclusion
Ce projet vous permet de configurer rapidement Qdrant dans un environnement Docker. Vous pouvez personnaliser le service avec des variables d'environnement et facilement le déployer grâce à Docker Compose.
