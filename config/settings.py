# config/settings.py
import os

# ─── MySQL Database ───────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "Lynx_123@",   # ← change this
    "database": "cyber_investigation"
}

# ─── Ollama (Fast LLM) ────────────────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL    = "phi3:mini"
OLLAMA_TIMEOUT  = 120

# ─── AirLLM (Deep Analysis) ───────────────────────────────────
AIRLLM_MODEL         = "meta-llama/Meta-Llama-3-8B-Instruct"
AIRLLM_COMPRESSION   = "4bit"
AIRLLM_MAX_NEW_TOKENS = 512

# ─── Embeddings ───────────────────────────────────────────────
EMBEDDING_MODEL      = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_BATCH_SIZE = 32

# ─── ChromaDB ─────────────────────────────────────────────────
CHROMA_PERSIST_DIR          = "./chroma_db"
CHROMA_EVIDENCE_COLLECTION  = "evidence"
CHROMA_KNOWLEDGE_COLLECTION = "knowledge"

# ─── Ingestion ────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".log", ".csv", ".docx"]
CHUNK_SIZE           = 500
CHUNK_OVERLAP        = 50
TOP_K_RETRIEVAL      = 5

# ─── Paths ────────────────────────────────────────────────────
BASE_DIR          = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base", "datasets")
UPLOAD_DIR        = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)

# ─── Logging ──────────────────────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FILE  = os.path.join(BASE_DIR, "system.log")

# ─── UI ───────────────────────────────────────────────────────
APP_TITLE   = "CyberIntel - Offline AI Investigation Assistant"
APP_ICON    = "🔍"