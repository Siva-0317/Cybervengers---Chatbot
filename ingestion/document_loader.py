# ingestion/document_loader.py
import os
import csv
import logging
from pathlib import Path
from config.settings import SUPPORTED_EXTENSIONS

logger = logging.getLogger(__name__)


def load_document(file_path: str) -> list[dict]:
    """
    Load any supported file and return a list of page/section dicts:
    [{ "content": "...", "metadata": { "source": "...", "page": N } }]
    """
    path = Path(file_path)
    ext  = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        return _load_pdf(file_path)
    elif ext in (".txt", ".log"):
        return _load_text(file_path)
    elif ext == ".csv":
        return _load_csv(file_path)
    elif ext == ".docx":
        return _load_docx(file_path)
    else:
        raise ValueError(f"No loader for: {ext}")


def _load_pdf(file_path: str) -> list[dict]:
    try:
        import fitz  # PyMuPDF
        doc    = fitz.open(file_path)
        pages  = []
        for i, page in enumerate(doc):
            text = page.get_text().strip()
            if text:
                pages.append({
                    "content":  text,
                    "metadata": {"source": file_path, "page": i + 1, "type": "pdf"}
                })
        logger.info(f"PDF loaded: {file_path} — {len(pages)} pages")
        return pages
    except Exception as e:
        logger.error(f"PDF load error: {e}")
        raise


def _load_text(file_path: str) -> list[dict]:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
        # Split large text files into logical sections (every 200 lines)
        lines    = content.splitlines()
        sections = []
        chunk_sz = 200
        for i in range(0, len(lines), chunk_sz):
            chunk = "\n".join(lines[i:i + chunk_sz]).strip()
            if chunk:
                sections.append({
                    "content":  chunk,
                    "metadata": {
                        "source":  file_path,
                        "section": i // chunk_sz + 1,
                        "type":    "log" if file_path.endswith(".log") else "text"
                    }
                })
        logger.info(f"Text/Log loaded: {file_path} — {len(sections)} sections")
        return sections
    except Exception as e:
        logger.error(f"Text load error: {e}")
        raise


def _load_csv(file_path: str) -> list[dict]:
    try:
        rows     = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader  = csv.DictReader(f)
            headers = reader.fieldnames or []
            all_rows = list(reader)

        # Group rows into chunks of 50 for embedding
        chunk_sz = 50
        for i in range(0, len(all_rows), chunk_sz):
            chunk_rows = all_rows[i:i + chunk_sz]
            # Convert rows to readable text
            text_lines = [" | ".join([f"{h}: {row.get(h,'')}" for h in headers])
                          for row in chunk_rows]
            rows.append({
                "content":  "\n".join(text_lines),
                "metadata": {
                    "source":  file_path,
                    "rows":    f"{i+1}-{min(i+chunk_sz, len(all_rows))}",
                    "type":    "csv"
                }
            })
        logger.info(f"CSV loaded: {file_path} — {len(rows)} chunks")
        return rows
    except Exception as e:
        logger.error(f"CSV load error: {e}")
        raise


def _load_docx(file_path: str) -> list[dict]:
    try:
        import docx
        doc   = docx.Document(file_path)
        pages = []
        # Group paragraphs into sections of ~50 paragraphs
        paras    = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        chunk_sz = 50
        for i in range(0, len(paras), chunk_sz):
            chunk = "\n".join(paras[i:i + chunk_sz])
            pages.append({
                "content":  chunk,
                "metadata": {
                    "source":  file_path,
                    "section": i // chunk_sz + 1,
                    "type":    "docx"
                }
            })
        logger.info(f"DOCX loaded: {file_path} — {len(pages)} sections")
        return pages
    except Exception as e:
        logger.error(f"DOCX load error: {e}")
        raise