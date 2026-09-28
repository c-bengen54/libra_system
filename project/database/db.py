from pathlib import Path
from dotenv import load_dotenv
import os
from psycopg_pool import ConnectionPool

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


pool = ConnectionPool(os.getenv("DATABASE_URL"), min_size=1, max_size=4, check=ConnectionPool.check_connection,)

def _execute(query, params=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)

def _fetch_all(query: str, params=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    
def _fetch_one(query:str, params=None):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()