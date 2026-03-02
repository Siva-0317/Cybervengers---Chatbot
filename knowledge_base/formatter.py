# knowledge_base/formatter.py
"""
Normalizes ALL records from all collectors into
a single uniform schema before embedding.
Applies cleaning, deduplication, and quality filtering.
"""
import re
import hashlib
import logging

logger = logging.getLogger(__name__)


def format_records(records: list[dict]) -> list[dict]:
    """
    Clean + deduplicate + quality filter all collected records.
    """
    cleaned   = [_clean(r) for r in records]
    filtered  = [r for r in cleaned if _quality_check(r)]
    deduped   = _deduplicate(filtered)

    logger.info(f"Formatting: {len(records)} raw → {len(filtered)} filtered → {len(deduped)} deduped")
    return deduped


def _clean(record: dict) -> dict:
    text = record.get("text", "")

    # Remove excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = text.strip()

    # Remove HTML artifacts
    text = re.sub(r"<[^>]+>", "", text)

    # Remove URLs (keep domain names)
    text = re.sub(r"https?://\S+", "[URL]", text)

    # Normalize quotes
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")

    record["text"] = text
    return record


def _quality_check(record: dict) -> bool:
    text = record.get("text", "")

    # Minimum length
    if len(text) < 50:
        return False

    # Maximum length (avoid huge chunks before chunking)
    if len(text) > 8000:
        record["text"] = text[:8000]

    # Must have actual words
    words = text.split()
    if len(words) < 10:
        return False

    # Skip if mostly symbols/numbers
    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.3:
        return False

    return True


def _deduplicate(records: list[dict]) -> list[dict]:
    seen_hashes = set()
    unique      = []
    for record in records:
        # Hash first 300 chars for near-duplicate detection
        text_key = record["text"][:300].lower().strip()
        h        = hashlib.md5(text_key.encode()).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            unique.append(record)
    return unique


def records_to_chunks(records: list[dict]) -> list[dict]:
    """
    Convert formatted records into ChromaDB-ready chunks.
    """
    chunks = []
    for record in records:
        chunks.append({
            "content":  record["text"],
            "metadata": {
                "source":   record.get("source", "unknown"),
                "category": record.get("category", "text"),
                **record.get("metadata", {})
            }
        })
    return chunks