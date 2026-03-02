# ingestion/embedder.py
import logging
import numpy as np
from config.settings import EMBEDDING_MODEL, EMBEDDING_BATCH_SIZE

logger = logging.getLogger(__name__)

_model = None  # singleton


def get_embedding_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
        logger.info("✅ Embedding model loaded")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text strings.
    Returns list of float vectors.
    """
    model      = get_embedding_model()
    embeddings = []

    # Process in batches to avoid OOM
    for i in range(0, len(texts), EMBEDDING_BATCH_SIZE):
        batch = texts[i:i + EMBEDDING_BATCH_SIZE]
        vecs  = model.encode(batch, show_progress_bar=False, convert_to_numpy=True)
        embeddings.extend(vecs.tolist())
        logger.debug(f"Embedded batch {i // EMBEDDING_BATCH_SIZE + 1}")

    logger.info(f"✅ Embedded {len(texts)} texts")
    return embeddings


def embed_query(query: str) -> list[float]:
    """Embed a single query string for retrieval."""
    model = get_embedding_model()
    vec   = model.encode([query], convert_to_numpy=True)
    return vec[0].tolist()