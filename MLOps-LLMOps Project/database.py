"""
SQLite database for storing chat history.
"""

import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/app/data/chat_history.db")


def init_db():
    """Initialize SQLite database and create tables if they don't exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


def save_prompt_response(user_id: str, prompt: str, response: str):
    """Save a chat interaction to the database."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO chat_history (user_id, prompt, response) VALUES (?, ?, ?)",
        (user_id, prompt, response)
    )
    
    conn.commit()
    conn.close()
