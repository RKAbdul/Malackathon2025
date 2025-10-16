"""
Database connection helpers. Uses environment variables.
Supports:
 - simple connect (user/password/dsn)
 - wallet-based connect if ORACLE_WALLET_PATH is provided
Provides a connection pool for efficient reuse.
"""

import os
import oracledb
from dotenv import load_dotenv

load_dotenv()
ORDS_BASE_URL = os.environ.get("ORDS_BASE_URL", "").rstrip("/")
DB_USER = os.environ.get("ORDS_BASIC_USER")
DB_PASSWORD = os.environ.get("ORDS_BASIC_PASS")

ORACLE_WALLET_PATH = os.environ.get("WALLET_PATH")
ORACLE_WALLET_PASSWORD = os.environ.get("WALLET_PASSWORD")

CONNECT_STRING = os.environ.get("CONNECT_STRING")

def init_pool():
    global pool
    
    pool = oracledb.create_pool(
    # If you want to connect using your wallet, uncomment the following line.
    config_dir=ORACLE_WALLET_PATH,
    user=DB_USER,
    password=DB_PASSWORD,
    dsn=CONNECT_STRING,
    # If THIN mode is needed and your Python version is 3.13 and above, uncomment the following lines.
    wallet_location=ORACLE_WALLET_PATH,
    wallet_password=ORACLE_WALLET_PASSWORD
    )

    print("Connection pool created")
    return pool

def get_conn():
    """
    Get a connection from the pool (caller should close it after use).
    """
    global pool
    
    try:
        if pool is None:
            pool = init_pool()
        return pool.acquire()
    except Exception as e:
        print("Error acquiring database connection", exc_info=e)
        raise
    
    
def __main__():
    # Simple test to verify connection
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT 'Connection Successful' FROM dual")
        result = cursor.fetchone()
        print(result[0])
    except Exception as e:
        print("Database connection test failed", exc_info=e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()