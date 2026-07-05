"""
config/db.py
-------------
Single place responsible for talking to MySQL.

We use PyMySQL (pure-Python MySQL driver, works great with XAMPP).
A new connection is opened per request and closed afterwards - this
keeps things simple and stateless, which matches the "stateless REST API"
design described in the architecture doc. For a small FYP project this
is more than fast enough; if performance ever becomes an issue, this is
the only file that would need to change to introduce a connection pool.
"""

import os
import pymysql
from pymysql.cursors import DictCursor


def get_db_connection():
    """
    Open and return a new PyMySQL connection using credentials from .env.

    - DictCursor is used so query results come back as dicts
      (e.g. {"id": 1, "name": "Alice"}) instead of plain tuples -
      this makes it trivial to jsonify() results straight from the DB.
    - autocommit=True means every successful statement is committed
      immediately. We don't currently need multi-statement transactions,
      so this keeps each route's code simple (no manual commit/rollback).
    """
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "aspar_db"),
        cursorclass=DictCursor,
        autocommit=True,
    )
    return connection


def test_connection():
    """
    Quick helper used by the /api/health route to confirm the app
    can actually reach MySQL. Returns True/False instead of raising,
    so the health route can report a clean status either way.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        conn.close()
        return True
    except Exception as e:
        print(f"[db] connection test failed: {e}")
        return False
