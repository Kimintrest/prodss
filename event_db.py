import sqlite3
from loaderof_db import event_db
def create_event_db():
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Event (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        time_created TEXT DEFAULT CURRENT_TIMESTAMP,
                        session_name STRING,
                        status INTEGER DEFAULT 0
                     )''')