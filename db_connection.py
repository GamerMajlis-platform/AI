import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def run_query(sql: str, params: tuple = ()):
    """Execute a SQL query and return results."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if results == []:
        return "None currently"
    return results

