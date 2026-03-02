# setup_project.py  ← run this once to bootstrap everything
import os
import subprocess
import sys

DIRS = [
    "config", "database", "ingestion",
    "knowledge_base/datasets", "engine",
    "features", "ui", "benchmarks", "uploads", "chroma_db"
]

def create_dirs():
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        init = os.path.join(d.split("/")[0], "__init__.py")
        open(init, "a").close()
    print("✅ Directories created")

def check_ollama():
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "phi3" in result.stdout:
        print("✅ Phi-3 Mini already pulled")
    else:
        print("⬇️  Pulling phi3:mini — this may take a while...")
        os.system("ollama pull phi3:mini")

def check_gpu():
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("⚠️  No GPU detected — will run on CPU (slower)")
    except ImportError:
        print("⚠️  PyTorch not installed yet — run requirements install first")

def check_mysql():
    try:
        import mysql.connector
        from config.settings import DB_CONFIG
        cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        conn = mysql.connector.connect(**cfg)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()
        conn.close()
        print(f"✅ MySQL database '{DB_CONFIG['database']}' ready")
    except Exception as e:
        print(f"❌ MySQL error: {e}")

if __name__ == "__main__":
    print("\n🚀 Setting up CyberIntel project...\n")
    create_dirs()
    check_gpu()
    check_mysql()
    check_ollama()
    print("\n✅ Setup complete! Proceed to Phase 1.\n")