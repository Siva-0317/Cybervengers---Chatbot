# knowledge_base/collectors/hf_collector.py
"""
Downloads datasets from HuggingFace and normalizes them
into a uniform format:
{
    "text":     "...",          # the knowledge content
    "source":   "SecQA",        # dataset name
    "category": "qa",           # qa | text | cve | instruction
    "metadata": { ... }         # any extra fields
}
"""
import logging
from datasets import load_dataset
from knowledge_base.dataset_sources import HUGGINGFACE_DATASETS

logger = logging.getLogger(__name__)


def collect_all_hf_datasets() -> list[dict]:
    all_records = []
    for ds_info in HUGGINGFACE_DATASETS:
        try:
            records = _collect_single(ds_info)
            all_records.extend(records)
            logger.info(f"✅ {ds_info['name']}: {len(records)} records")
        except Exception as e:
            logger.warning(f"⚠️  Skipped {ds_info['name']}: {e}")
    logger.info(f"Total HuggingFace records collected: {len(all_records)}")
    return all_records


def _collect_single(ds_info: dict) -> list[dict]:
    kwargs = {"split": ds_info.get("split", "train")}
    if ds_info.get("config"):
        kwargs["name"] = ds_info["config"]

    # Load with trust_remote_code for some datasets
    try:
        ds = load_dataset(ds_info["id"], **kwargs, trust_remote_code=True)
    except Exception:
        ds = load_dataset(ds_info["id"], **kwargs)

    max_records = ds_info.get("max_records", None)
    if max_records:
        ds = ds.select(range(min(max_records, len(ds))))

    dtype    = ds_info.get("type", "text")
    name     = ds_info["name"]
    records  = []

    for row in ds:
        text = _extract_text(row, dtype)
        if text and len(text.strip()) > 30:
            records.append({
                "text":     text.strip(),
                "source":   name,
                "category": dtype,
                "metadata": {"dataset_id": ds_info["id"]}
            })

    return records


def _extract_text(row: dict, dtype: str) -> str:
    """
    Normalize different dataset schemas into plain text.
    """
    # ── Q&A format ──────────────────────────────────────────
    if dtype == "qa":
        q = row.get("question", row.get("Question", ""))
        a = row.get("answer",   row.get("Answer",   row.get("correct_answer", "")))
        choices = row.get("choices", row.get("options", None))
        if choices:
            choice_text = "\n".join([f"  {chr(65+i)}. {c}" for i, c in enumerate(choices)])
            return f"Question: {q}\nChoices:\n{choice_text}\nAnswer: {a}"
        return f"Question: {q}\nAnswer: {a}" if q and a else q or a

    # ── Instruction format ───────────────────────────────────
    if dtype == "instruction":
        system = row.get("system", "")
        user   = row.get("user",   row.get("instruction", row.get("input", "")))
        asst   = row.get("assistant", row.get("output", row.get("response", "")))
        parts  = []
        if system: parts.append(f"[SYSTEM]: {system}")
        if user:   parts.append(f"[USER]: {user}")
        if asst:   parts.append(f"[ASSISTANT]: {asst}")
        return "\n".join(parts)

    # ── CVE format ───────────────────────────────────────────
    if dtype == "cve":
        cve_id = row.get("CVE_ID",      row.get("cve_id",      ""))
        desc   = row.get("description", row.get("Description", row.get("summary", "")))
        cvss   = row.get("cvss_score",  row.get("CVSS",        ""))
        cwe    = row.get("CWE",         row.get("cwe",         ""))
        text   = f"CVE ID: {cve_id}\n"
        if desc:  text += f"Description: {desc}\n"
        if cvss:  text += f"CVSS Score: {cvss}\n"
        if cwe:   text += f"CWE: {cwe}\n"
        return text

    # ── Plain text ───────────────────────────────────────────
    for key in ["text", "content", "body", "passage", "document", "data"]:
        if key in row and row[key]:
            return str(row[key])

    # Fallback: join all string fields
    return " ".join(str(v) for v in row.values() if isinstance(v, str) and len(str(v)) > 10)