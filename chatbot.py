import os
from openai import OpenAI
from qdrant_client import QdrantClient
from dotenv import load_dotenv


# Charger les variables d'environnement
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY") or None
)


def embed(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text, encoding_format="float"
    )
    return response.data[0].embedding


def chat_loop():
    print(
        "Bienvenue dans le chatbot support des paroles de Vald ! "
        "Tape 'exit' pour quitter.\n"
    )
    while True:
        user_query = input("Votre question > ").strip()
        if user_query.lower() == "exit":
            print("Au revoir !")
            break

        query_vec = embed(user_query)
        hits = qdrant.search(
            collection_name="lyrics_support_channel",
            query_vector=query_vec,
            limit=1,
            with_payload=True,
        )

        if hits:
            context = hits[0].payload.get("text")
        else:
            context = "Aucun contexte trouvé."

        prompt = (
            "Tu es un chatbot chargé de faire du support pour une société "
            "d'explication de paroles de chanson.\n"
            f"Voici la question de l'utilisateur : {user_query}\n"
            f"Voici un extrait de chat à utiliser comme contexte : {context}\n"
            "Réponds de façon claire, concise.\n"
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        print("\n→ Réponse du bot :", completion.choices[0].message.content)
        print("\nPose une autre question ou tape 'exit' pour quitter.\n")


if __name__ == "__main__":
    chat_loop()
