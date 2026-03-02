# ingestion/ingestor.py
"""
Main orchestrator: file → load → chunk → embed → ChromaDB + MySQL
"""
import os
import logging
from pathlib import Path

from ingestion.document_loader import load_document
from ingestion.chunker          import chunk_documents
from ingestion.embedder         import embed_texts
from ingestion.vector_store     import add_chunks
from database.crud              import add_evidence, update_evidence_summary
from config.settings            import CHROMA_EVIDENCE_COLLECTION

logger = logging.getLogger(__name__)


def ingest_file(file_path: str, case_id: int) -> dict:
    """
    Full pipeline: load + chunk + embed + store.
    Returns summary dict with evidence_id and chunk_count.
    """
    path      = Path(file_path)
    file_name = path.name
    file_type = path.suffix.lower().lstrip(".")

    logger.info(f"Ingesting: {file_name} for case {case_id}")

    # Step 1 — Load
    documents = load_document(file_path)
    if not documents:
        raise ValueError(f"No content extracted from {file_name}")

    # Step 2 — Chunk
    chunks = chunk_documents(documents)

    # Step 3 — Embed
    texts      = [c["content"] for c in chunks]
    embeddings = embed_texts(texts)

    # Step 4 — Store in ChromaDB (tag with case_id for filtered retrieval)
    for chunk in chunks:
        chunk["metadata"]["case_id"] = str(case_id)
        chunk["metadata"]["file_name"] = file_name

    vector_ids = add_chunks(chunks, CHROMA_EVIDENCE_COLLECTION, embeddings)

    # Step 5 — Save record to MySQL
    evidence_id = add_evidence(
        case_id     = case_id,
        file_name   = file_name,
        file_type   = file_type,
        file_path   = str(file_path),
        chunk_count = len(chunks)
    )

    # Step 6 — Save vector IDs back to MySQL
    update_evidence_summary(evidence_id, summary="", vector_ids=vector_ids)

    result = {
        "evidence_id":  evidence_id,
        "file_name":    file_name,
        "chunk_count":  len(chunks),
        "vector_ids":   vector_ids,
        "status":       "success"
    }
    logger.info(f"✅ Ingested {file_name}: {len(chunks)} chunks, evidence_id={evidence_id}")
    return result


def ingest_knowledge_file(file_path: str, source_tag: str = "knowledge") -> dict:
    """
    Ingest into the permanent knowledge collection (IT Act, MITRE, CVE, etc.)
    No case_id required.
    """
    from ingestion.vector_store import add_chunks
    from config.settings import CHROMA_KNOWLEDGE_COLLECTION

    documents = load_document(file_path)
    chunks    = chunk_documents(documents)
    texts     = [c["content"] for c in chunks]

    for chunk in chunks:
        chunk["metadata"]["source_tag"] = source_tag

    embeddings = embed_texts(texts)
    ids        = add_chunks(chunks, CHROMA_KNOWLEDGE_COLLECTION, embeddings)

    logger.info(f"✅ Knowledge ingested: {file_path} — {len(chunks)} chunks")
    return {"file": file_path, "chunk_count": len(chunks), "ids": ids}