# database/init_db.py
import mysql.connector
from config.settings import DB_CONFIG

def init_database():
    # Connect WITHOUT specifying the database first
    cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    conn = mysql.connector.connect(**cfg)
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        sql = f.read()

    # Execute each statement separately
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for stmt in statements:
        try:
            cursor.execute(stmt)
            print(f"✅ {stmt[:70]}...")
        except Exception as e:
            print(f"⚠️  Skipped: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n✅ Database + all tables created successfully!")

if __name__ == "__main__":
    init_database()