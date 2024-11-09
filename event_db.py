import random
import sqlite3
from loaderof_db import event_db
import string
import json

def create_event_db():
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS event (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        time_created TEXT DEFAULT CURRENT_TIMESTAMP,
                        status INTEGER DEFAULT 0,
                        admin INTEGER NOT NULL,
                        unique_code NOT NULL,
                        users_list TEXT
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

def add_event(name, admin):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO event (name, admin, unique_code) VALUES (?, ?, ?, ?)",
                   (name, admin, int(random.choices(string.digits, k=6))))
    conn.commit()
    conn.close()


def get_event_by_userlist(unique_code):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Event WHERE unique_code = ?''', (unique_code))
    parametrs = cursor.fetchone()
    conn.close()
    return parametrs


def add_user_by_event_uniquecode(user_id, users_uniqode):
    conn = sqlite3.connect()
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT users_list FROM Events WHERE unique_code = ?''', (users_uniqode))
        lst = cursor.fetchone()
        tsl = list(json.dumps(lst))
        tsl.append(user_id)
        conn.close()
        return json.loads(tsl)
    except Exception:
        conn.close()
        return "Такого события не существует"
    

def get_unique_code():
    conn = sqlite3.connect()
    cursor = conn.cursor()
    
create_event_db()