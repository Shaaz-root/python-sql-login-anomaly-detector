import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "login_events.db"

def create_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    with create_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS login_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                username TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('SUCCESS', 'FAILED'))
            )
        """)

def insert_event(event):
    with create_connection() as connection:
        connection.execute("""
            INSERT INTO login_events (timestamp, username, ip_address, status)
            VALUES (?, ?, ?, ?)
        """, (
            event["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            event["username"],
            event["ip_address"], 
            event["status"], ))

def get_all_events():
    

    with create_connection() as connection:
        rows = connection.execute("""
            SELECT id, timestamp, username, ip_address, status
            FROM login_events
            ORDER BY timestamp
        """).fetchall()

        return [dict(row) for row in rows]