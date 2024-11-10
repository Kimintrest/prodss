import random
import sqlite3
import string
from loaderof_db import event_db
import json

def create_event_db():
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS event (
                            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            status INTEGER DEFAULT 0,
                            admin INTEGER NOT NULL,
                            unique_code INTEGER NOT NULL UNIQUE,
                            users_list TEXT
                         )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred during database creation: {e}")
    finally:
        if conn:
            conn.close()


def get_admin_by_event_id(event_id):
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute("SELECT admin FROM event WHERE event_id = ?", (event_id,))
        admin = cursor.fetchone()
        return admin[0] if admin else None
    except sqlite3.Error as e:
        print(f"An error occurred while fetching admin: {e}")
        return None
    finally:
        if conn:
            conn.close()


def generate_unique_code():
    while True:
        unique_code = random.randint(100000, 9999999)  # Генерация 6-значного числа
        if not code_exists(unique_code):
            return unique_code


def code_exists(unique_code):
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM event WHERE unique_code = ?", (unique_code,))
        exists = cursor.fetchone() is not None
        return exists
    except sqlite3.Error as e:
        print(f"An error occurred while checking unique code: {e}")
        return False
    finally:
        if conn:
            conn.close()


def add_event(name, admin):
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO event (name, admin, unique_code, users_list) VALUES (?, ?, ?, ?)",
                       (name, admin, generate_unique_code(), '[]'))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while adding event: {e}")
    finally:
        if conn:
            conn.close()


def get_event_by_uniquecode(unique_code):
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM event WHERE unique_code = ?''', (unique_code,))
        parameters = cursor.fetchone()
        return parameters
    except sqlite3.Error as e:
        print(f"An error occurred while fetching event by unique code: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_user_by_event_uniquecode(user_id, users_uniqode):
    conn = None
    try:
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

    except sqlite3.Error as e:
        print(f"An error occurred while adding user to event: {e}")
    finally:
        if conn:
            conn.close()


def update_event_status_by_uniquecode(event_id, new_status):
    conn = None
    try:
        conn = sqlite3.connect(event_db)
        cursor = conn.cursor()
        cursor.execute('''UPDATE event SET status = ? WHERE event_id = ?''', (new_status, event_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while updating event status: {e}")
    finally:
        if conn:
            conn.close()

create_event_db()
