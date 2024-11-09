import random
import sqlite3
from loaderof_db import event_db
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
                        unique_code INTEGER NOT NULL UNIQUE,
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


def generate_unique_code():
    while True:
        unique_code = random.randint(100000, 9999999)  # Генерация 6-значного числа
        if not code_exists(unique_code):
            return unique_code


def code_exists(unique_code):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM event WHERE unique_code = ?", (unique_code,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def add_event(name, admin):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO event (name, admin, unique_code) VALUES (?, ?, ?, ?)",
                   (name, admin, int(random.choices(string.digits, k=6))))
    conn.commit()
    conn.close()


def get_event_by_uniquecode(unique_code):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM event WHERE unique_code = ?''', (unique_code,))
    parameters = cursor.fetchone()
    conn.close()
    return parameters


def add_user_by_event_uniquecode(user_id, users_uniqode):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT users_list FROM event WHERE unique_code = ?''', (users_uniqode,))
    lst = cursor.fetchone()

    if lst and lst[0]:
        tsl = json.loads(lst[0])
    else:
        tsl = []

    tsl.append(user_id)

    new_users_list = json.dumps(tsl)
    cursor.execute('''UPDATE event SET users_list = ? WHERE unique_code = ?''', (new_users_list, users_uniqode))
    conn.commit()
    conn.close()


def update_event_status_by_uniquecode(event_id, new_status):
    conn = sqlite3.connect(event_db)
    cursor = conn.cursor()
    cursor.execute('''UPDATE event SET status = ? WHERE event_id = ?''', (new_status, event_id))
    conn.commit()
    conn.close()

create_event_db()
