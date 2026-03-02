# database/db_connection.py
import mysql.connector
from mysql.connector import pooling
import logging
from config.settings import DB_CONFIG

logger = logging.getLogger(__name__)

class DatabaseConnection:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name="cyberintel_pool",
                    pool_size=5,
                    **DB_CONFIG
                )
                logger.info("✅ MySQL connection pool created")
            except mysql.connector.Error as e:
                logger.error(f"❌ MySQL pool creation failed: {e}")
                raise
        return cls._pool

    @classmethod
    def get_connection(cls):
        return cls.get_pool().get_connection()

import os

def init_database():
    with open("database/schema.sql", "r") as f:
        sql = f.read()
    
    # Split by semicolon and run each statement
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for stmt in statements:
        try:
            execute_query(stmt)
            print(f"✅ Executed: {stmt[:60]}...")
        except Exception as e:
            print(f"⚠️  {e}")

def get_db():
    """Context manager style — use in with statements"""
    return DatabaseConnection.get_connection()


def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """
    Generic query executor.
    fetch=True  → returns rows
    fetch=False → returns lastrowid
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        return result
    except mysql.connector.Error as e:
        conn.rollback()
        logger.error(f"Query failed: {e}\nQuery: {query}\nParams: {params}")
        raise
    finally:
        cursor.close()
        conn.close()


def execute_many(query: str, params_list: list):
    """Batch insert/update"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as e:
        conn.rollback()
        logger.error(f"Batch query failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()