# brain/memory.py

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "memory.db")

def init_memory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            key TEXT UNIQUE,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def remember(key, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO memory (timestamp, key, value)
        VALUES (?, ?, ?)
    ''', (datetime.now().isoformat(), key.lower(), value))
    conn.commit()
    conn.close()

def recall(key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM memory WHERE key = ?', (key.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
