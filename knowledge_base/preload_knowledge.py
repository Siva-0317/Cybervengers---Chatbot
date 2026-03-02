# knowledge_base/preload_knowledge.py
"""
MASTER RUNNER — Execute this once to build the entire knowledge base.
Run: python -m knowledge_base.preload_knowledge
"""
import logging
import time
from config.settings import CHROMA_KNOWLEDGE_COLLECTION

from knowledge_base.collectors.hf_collector     import collect_all_hf_datasets
from knowledge_base.collectors.mitre_collector  import parse_mitre
from knowledge_base.collectors.nvd_collector    import parse_nvd_feeds
from knowledge_base.collectors.custom_qa_builder import get_custom_qa_records
from knowledge_base.formatter                   import format_records, records_to_chunks
from ingestion.embedder                         import embed_texts
from ingestion.vector_store                     import add_chunks, get_collection_count, reset_collection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


def build_knowledge_base(skip_hf: bool = False, skip_nvd: bool = False):
    """
    Full pipeline to build the offline knowledge base.

    Args:
        skip_hf:  Skip HuggingFace downloads (useful if already done)
        skip_nvd: Skip NVD downloads (large files, ~400MB each)
    """
    start_time = time.time()
    all_records = []

    # ── 1. Custom Q&A (most targeted, always include) ────────
    logger.info("── Loading custom investigation Q&A pairs...")
    custom = get_custom_qa_records()
    all_records.extend(custom)
    logger.info(f"   Custom QA: {len(custom)} records")

    # ── 2. MITRE ATT&CK ──────────────────────────────────────
    logger.info("── Parsing MITRE ATT&CK framework...")
    try:
        mitre = parse_mitre()
        all_records.extend(mitre)
    except Exception as e:
        logger.warning(f"MITRE failed: {e}")

    # ── 3. NVD CVE Feeds ─────────────────────────────────────
    if not skip_nvd:
        logger.info("── Downloading & parsing NVD CVE feeds (this takes a while)...")
        try:
            cves = parse_nvd_feeds(max_per_feed=10000)
            all_records.extend(cves)
        except Exception as e:
            logger.warning(f"NVD failed: {e}")
    else:
        logger.info("── Skipping NVD CVE feeds")

    # ── 4. HuggingFace Datasets ───────────────────────────────
    if not skip_hf:
        logger.info("── Downloading HuggingFace datasets...")
        try:
            hf_records = collect_all_hf_datasets()
            all_records.extend(hf_records)
        except Exception as e:
            logger.warning(f"HuggingFace collection failed: {e}")
    else:
        logger.info("── Skipping HuggingFace datasets")

    # ── 5. Format + Deduplicate ───────────────────────────────
    logger.info(f"── Total raw records collected: {len(all_records)}")
    logger.info("── Formatting and deduplicating...")
    formatted = format_records(all_records)
    logger.info(f"── After formatting: {len(formatted)} records")

    # ── 6. Convert to chunks ──────────────────────────────────
    chunks = records_to_chunks(formatted)

    # ── 7. Embed in batches ───────────────────────────────────
    logger.info(f"── Embedding {len(chunks)} chunks (this is the slow part)...")
    texts      = [c["content"] for c in chunks]
    embeddings = embed_texts(texts)

    # ── 8. Store in ChromaDB (reset first to prevent duplicates) ──
    logger.info("── Resetting ChromaDB knowledge collection (prevents duplicates)...")
    reset_collection(CHROMA_KNOWLEDGE_COLLECTION)
    logger.info("── Storing in ChromaDB knowledge collection...")
    add_chunks(chunks, CHROMA_KNOWLEDGE_COLLECTION, embeddings)

    # ── Summary ───────────────────────────────────────────────
    total_time = round(time.time() - start_time, 1)
    final_count = get_collection_count(CHROMA_KNOWLEDGE_COLLECTION)

    print("\n" + "="*60)
    print("✅ KNOWLEDGE BASE BUILD COMPLETE")
    print("="*60)
    print(f"  Total records processed : {len(all_records)}")
    print(f"  After deduplication     : {len(formatted)}")
    print(f"  Chunks in ChromaDB      : {final_count}")
    print(f"  Time taken              : {total_time}s ({total_time/60:.1f} min)")
    print("="*60)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build CyberIntel knowledge base")
    parser.add_argument("--skip-hf",  action="store_true", help="Skip HuggingFace downloads")
    parser.add_argument("--skip-nvd", action="store_true", help="Skip NVD CVE downloads")
    args = parser.parse_args()

    build_knowledge_base(skip_hf=args.skip_hf, skip_nvd=args.skip_nvd)