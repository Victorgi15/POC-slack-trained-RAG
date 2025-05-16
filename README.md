# Chatbot Support Paroles — Projet Python avec Qdrant & Docker

Un prototype Python qui transforme un canal Slack de support en chatbot question-réponse sur des paroles de chanson.  
Le projet **génère des embeddings** à partir des threads Slack avec OpenAI (`text-embedding-3-small`), stocke les vecteurs dans **Qdrant** via Docker Compose, puis permet de discuter avec GPT en récupérant le contexte le plus pertinent.

---

## ✨ Fonctionnalités

- Ingestion du fichier Slack JSON (`lyrics_support_channel.json`), regroupement par thread (questions + réponses)
- Création d’embeddings 1536 dimensions avec le modèle OpenAI `text-embedding-3-small`
- Stockage des embeddings dans une collection locale **Qdrant** nommée `lyrics_support_channel`
- Chatbot CLI léger : recherche hybride dans Qdrant → génération de réponses GPT contextualisées
- Déploiement local simple avec Docker Compose pour Qdrant

---

## 🗂️ Structure du projet

```
.
├── docker-compose.yml            # Configuration du service Qdrant
├── embedded-slack-channel.py    # Pipeline d’ingestion et indexation des threads Slack
├── chatbot.py                   # Chatbot interactif en console
├── lyrics_support_channel.json  # Transcript Slack exemple
├── requirements.txt             # Dépendances Python
└── .env                         # Variables d’environnement (API keys, URLs)
```

---

## 🚀 Démarrage rapide

### 1. Prérequis

- Python 3.8+
- Docker & Docker Compose
- Clé API OpenAI valide
- Accès Qdrant local (via Docker) ou distant

### 2. Cloner et installer

```bash
git clone <votre_fork_url>
cd POC-slack-trained-RAG
python -m venv .venv
source .venv/bin/activate   # ou .\.venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

### 3. Configurer l’environnement

Créer un fichier `.env` à la racine :

```env
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
QDRANT_PORT=6333
QDRANT_API_KEY=               # Optionnel si Qdrant local sans auth
OPENAI_MODEL=text-embedding-3-small
```

### 4. Démarrer Qdrant avec Docker Compose

```bash
docker-compose up -d
```

Qdrant sera accessible sur `http://localhost:6333` par défaut.

### 5. Indexer les threads Slack

```bash
python embedded-slack-channel.py
```

Cela va parser le JSON, créer les embeddings et les insérer dans Qdrant.

### 6. Lancer le chatbot

```bash
python chatbot.py
```

Exemple d’interaction :

```
Bienvenue dans le chatbot support paroles ! Tapez 'exit' pour quitter.
> Que veut dire cette phrase dans la chanson ?
→ Réponse : ...
```

---

## 🔧 Personnalisation

| Élément à modifier               | Fichier concerné                                   |
| -------------------------------- | -------------------------------------------------- |
| Nom de la collection Qdrant      | `embedded-slack-channel.py` & `chatbot.py`         |
| Modèle d’embedding OpenAI        | Fonction d’appel OpenAI dans les deux scripts      |
| Fichier source des conversations | Remplacer `lyrics_support_channel.json`            |
| Limite de résultats de recherche | Dans `chatbot.py`, méthode `qdrant.search()`       |
| Modèle et prompt GPT             | Dans `chatbot.py`, appel `OpenAI chat completions` |

---

## 📜 Licence

Projet sous licence ISC — voir `requirements.txt` ou fichier dédié.

---

## 🙏 Remerciements

- **OpenAI** pour embeddings et GPT
- **Qdrant** pour la recherche vectorielle
- **Docker & Docker Compose** pour l’orchestration locale
- **Tom Andrieu**, pour ses explications claires sur le fonctionnement des RAG

Ce projet est une démonstration simple et complète de pipeline RAG avec Slack, Qdrant et GPT pour un chatbot support paroles.
