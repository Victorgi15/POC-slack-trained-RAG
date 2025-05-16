import uuid
import json
from typing import List, Dict
import os
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv


# Charger les variables d'environnement
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY") or None
)

# Charger le fichier JSON complet
with open("lyrics_support_channel.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraire la liste des messages
messages = data["messages"]


def group_threads(msgs):
    by_thread = {}

    for msg in msgs:
        thread_ts = msg.get("thread_ts")
        if not thread_ts:
            # C'est un message principal (question)
            by_thread[msg["ts"]] = {"question": msg, "answers": []}
        else:
            # C'est une réponse dans un thread
            if thread_ts in by_thread:
                by_thread[thread_ts]["answers"].append(msg)
            else:
                print(
                    f"Warning: thread {thread_ts} not found\n"
                    f"for message ts={msg['ts']}"
                )

    return list(by_thread.values())


# Fonction d'embedding
model_name = os.getenv(
    "OPENAI_MODEL", "text-embedding-3-small"
)  # valeur par défaut si variable absente


def embed(text: str) -> List[float]:
    try:
        response = client.embeddings.create(model=model_name, input=text)
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Erreur lors de la création de l'embedding : {e}")
        return []


# Construction des vecteurs
def build_points(threads: List[Dict]) -> List[PointStruct]:
    points = []

    for thread in threads:
        text_block = f"Q: {thread['question']['text']}\n\n"
        for answer in thread["answers"]:
            text_block += f"A: {answer['text']}\n"

        vector = embed(text_block)
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "text": text_block,
                "asker": thread["question"]["user"],
                "thread_ts": thread["question"]["ts"],
            },
        )
        points.append(point)

    return points


def main():
    # Créer la collection si elle n'existe pas déjà
    collection_name = "lyrics_support_channel"
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

    threads = group_threads(messages)
    print(f"Found {len(threads)} threads")

    points = build_points(threads)

    # On peut uploader les points en batch (ici par 10 pour éviter les timeout)
    for i in range(0, len(points), 10):
        batch = points[i:i+10]
        qdrant.upsert(collection_name=collection_name, points=batch)
        print(f"Upserted batch {i // 10 + 1}")


if __name__ == "__main__":
    main()
