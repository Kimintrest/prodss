import sqlite3
from loaderof_db import event_db

def create_event_db():
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS event (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        time_created TEXT DEFAULT CURRENT_TIMESTAMP,
                        session_name TEXT,
                        status INTEGER DEFAULT 0,
                        admin INTEGER NOT NULL
                     )''')
    conn.commit()
    conn.close()

def get_admin_by_event_id(event_id):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute("SELECT admin FROM event WHERE event_id = ?", (event_id,))
    admin = cursor.fetchone()
    conn.close()
    return admin[0] if admin else None

def add_event(name, session_name, admin):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO event (name, session_name, admin) VALUES (?, ?, ?)",
                   (name, session_name, admin))
    conn.commit()
    conn.close()
