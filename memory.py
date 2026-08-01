import os
import chromadb
from sentence_transformers import SentenceTransformer

# Folder for storing vector database
db_folder = "memory_db"

if not os.path.exists(db_folder):
    os.makedirs(db_folder)

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=db_folder)

collection = client.get_or_create_collection(
    name="user_memory"
)


def save_memory(text):

    vector = model.encode(text).tolist()

    memory_id = str(collection.count() + 1)

    collection.add(
        ids=[memory_id],
        documents=[text],
        embeddings=[vector]
    )


def search_memory(question):

    if collection.count() == 0:
        return ""

    vector = model.encode(question).tolist()

    result = collection.query(
        query_embeddings=[vector],
        n_results=3
    )

    docs = result["documents"][0]

    if len(docs) == 0:
        return ""

    return "\n".join(docs)


def get_memory():

    data = collection.get()

    return data["documents"]


def delete_memory():

    ids = collection.get()["ids"]

    if len(ids) > 0:
        collection.delete(ids=ids)