# ingestion/chunker.py
import logging
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Takes loaded document sections and splits them into
    embedding-ready chunks with overlap.
    """
    chunks = []
    for doc in documents:
        text     = doc["content"]
        metadata = doc["metadata"]
        doc_chunks = _split_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(doc_chunks):
            chunks.append({
                "content":  chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": i,
                    "total_chunks": len(doc_chunks)
                }
            })
    logger.info(f"Chunking complete: {len(documents)} sections → {len(chunks)} chunks")
    return chunks


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Word-level sliding window chunker.
    chunk_size and overlap are in approximate word counts.
    """
    words  = text.split()
    chunks = []
    start  = 0

    while start < len(words):
        end   = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            chunks.append(chunk)
        if end == len(words):
            break
        start += chunk_size - overlap  # slide with overlap

    return chunks