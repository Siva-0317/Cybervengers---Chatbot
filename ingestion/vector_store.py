# ingestion/vector_store.py
import uuid
import logging
import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import CHROMA_PERSIST_DIR, CHROMA_EVIDENCE_COLLECTION, CHROMA_KNOWLEDGE_COLLECTION, TOP_K_RETRIEVAL

logger = logging.getLogger(__name__)

_client = None  # singleton


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        logger.info(f"✅ ChromaDB client initialized at {CHROMA_PERSIST_DIR}")
    return _client


def get_collection(collection_name: str):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )


def add_chunks(chunks: list[dict], collection_name: str, embeddings: list[list[float]]) -> list[str]:
    """
    Add embedded chunks to ChromaDB.
    Returns list of generated IDs.
    """
    collection = get_collection(collection_name)
    ids        = [str(uuid.uuid4()) for _ in chunks]
    documents  = [c["content"]  for c in chunks]
    metadatas  = [c["metadata"] for c in chunks]

    # ChromaDB add in batches of 500
    batch_sz = 500
    for i in range(0, len(ids), batch_sz):
        collection.add(
            ids        = ids[i:i + batch_sz],
            embeddings = embeddings[i:i + batch_sz],
            documents  = documents[i:i + batch_sz],
            metadatas  = metadatas[i:i + batch_sz]
        )
    logger.info(f"✅ Added {len(ids)} chunks to collection '{collection_name}'")
    return ids


def query_collection(query_embedding: list[float], collection_name: str,
                     n_results: int = None, where: dict = None) -> list[dict]:
    """
    Semantic search in ChromaDB.
    Returns list of { content, metadata, distance } dicts.
    """
    collection = get_collection(collection_name)
    n          = n_results or TOP_K_RETRIEVAL

    kwargs = dict(
        query_embeddings = [query_embedding],
        n_results        = n,
        include          = ["documents", "metadatas", "distances"]
    )
    if where:
        kwargs["where"] = where

    results = collection.query(**kwargs)

    # Flatten into clean list
    hits = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        hits.append({
            "content":  doc,
            "metadata": meta,
            "score":    round(1 - dist, 4)   # cosine similarity (higher = better)
        })

    return hits


def reset_collection(collection_name: str):
    """Delete and recreate a collection — wipes all existing data."""
    client = get_chroma_client()
    try:
        client.delete_collection(collection_name)
        logger.info(f"🗑️  Dropped existing collection '{collection_name}'")
    except Exception:
        pass  # collection didn't exist yet
    client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    logger.info(f"✅ Fresh collection '{collection_name}' created")


def delete_by_ids(ids: list[str], collection_name: str):
    collection = get_collection(collection_name)
    collection.delete(ids=ids)
    logger.info(f"Deleted {len(ids)} chunks from '{collection_name}'")


def get_collection_count(collection_name: str) -> int:
    return get_collection(collection_name).count()