from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_model():
    """Load the embedding model only when memory is first used."""
    return SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="memory_db")

collection = client.get_or_create_collection(
    name="chat_memory"
)

def create_database():
    return collection


def save_memory(text, memory_id):
    embedding = get_model().encode(text).tolist()

    collection.add(
        ids=[memory_id],
        embeddings=[embedding],
        documents=[text]
    )


def search_memory(query, top_k=5):
    if collection.count() == 0:
        return []

    embedding = get_model().encode(query).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(top_k, collection.count())
    )

    if len(results["documents"]) == 0:
        return []

    return results["documents"][0]
