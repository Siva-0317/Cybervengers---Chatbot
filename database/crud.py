# database/crud.py
import json
import logging
from datetime import datetime
from database.db_connection import execute_query, execute_many

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
#  CASES
# ══════════════════════════════════════════════════════════════

def create_case(case_name: str, investigator: str, description: str = "") -> int:
    query = """
        INSERT INTO cases (case_name, investigator, description)
        VALUES (%s, %s, %s)
    """
    case_id = execute_query(query, (case_name, investigator, description))
    logger.info(f"Case created: ID={case_id}, Name={case_name}")
    return case_id


def get_case(case_id: int) -> dict:
    return execute_query(
        "SELECT * FROM cases WHERE case_id = %s", (case_id,), fetch=True
    )


def get_all_cases() -> list:
    return execute_query(
        "SELECT * FROM cases ORDER BY created_at DESC", fetch=True
    )


def update_case_status(case_id: int, status: str):
    execute_query(
        "UPDATE cases SET status = %s WHERE case_id = %s", (status, case_id)
    )


# ══════════════════════════════════════════════════════════════
#  EVIDENCE
# ══════════════════════════════════════════════════════════════

def add_evidence(case_id: int, file_name: str, file_type: str,
                 file_path: str, chunk_count: int = 0) -> int:
    query = """
        INSERT INTO evidence (case_id, file_name, file_type, file_path, chunk_count)
        VALUES (%s, %s, %s, %s, %s)
    """
    eid = execute_query(query, (case_id, file_name, file_type, file_path, chunk_count))
    logger.info(f"Evidence added: ID={eid}, File={file_name}")
    return eid


def update_evidence_summary(evidence_id: int, summary: str, vector_ids: list):
    execute_query(
        "UPDATE evidence SET summary = %s, vector_ids = %s WHERE evidence_id = %s",
        (summary, json.dumps(vector_ids), evidence_id)
    )


def get_evidence_by_case(case_id: int) -> list:
    return execute_query(
        "SELECT * FROM evidence WHERE case_id = %s ORDER BY uploaded_at DESC",
        (case_id,), fetch=True
    )


def get_evidence(evidence_id: int) -> dict:
    rows = execute_query(
        "SELECT * FROM evidence WHERE evidence_id = %s", (evidence_id,), fetch=True
    )
    return rows[0] if rows else None


# ══════════════════════════════════════════════════════════════
#  QUERY LOGS (Audit Trail)
# ══════════════════════════════════════════════════════════════

def log_query(case_id: int, investigator: str, query_text: str,
              response_text: str, model_used: str, sources_cited: list = None) -> int:
    query = """
        INSERT INTO query_logs
            (case_id, investigator, query_text, response_text, model_used, sources_cited)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    lid = execute_query(query, (
        case_id, investigator, query_text, response_text,
        model_used, json.dumps(sources_cited or [])
    ))
    return lid


def get_query_logs(case_id: int) -> list:
    return execute_query(
        "SELECT * FROM query_logs WHERE case_id = %s ORDER BY timestamp DESC",
        (case_id,), fetch=True
    )


# ══════════════════════════════════════════════════════════════
#  LAW REFERENCES
# ══════════════════════════════════════════════════════════════

def add_law_reference(act_name: str, section: str, title: str,
                      description: str, punishment: str = "", keywords: str = "") -> int:
    query = """
        INSERT INTO law_references (act_name, section, title, description, punishment, keywords)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_query(query, (act_name, section, title, description, punishment, keywords))


def bulk_insert_laws(records: list):
    """records: list of tuples (act_name, section, title, description, punishment, keywords)"""
    query = """
        INSERT IGNORE INTO law_references
            (act_name, section, title, description, punishment, keywords)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute_many(query, records)


def search_law_references(keyword: str) -> list:
    return execute_query(
        "SELECT * FROM law_references WHERE keywords LIKE %s OR title LIKE %s LIMIT 10",
        (f"%{keyword}%", f"%{keyword}%"), fetch=True
    )


def get_all_laws() -> list:
    return execute_query("SELECT * FROM law_references", fetch=True)