import json
import sqlite3
import time

from loaderof_db import users_db

def create_users_db():
    conn = None
    try:
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            phone_number TEXT NOT NULL UNIQUE,
                            card_number TEXT DEFAULT NULL,
                            event_list TEXT
                         )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred during database creation: {e}")
    finally:
        if conn:
            conn.close()


def user_register(username, phone_number, card_number=None):
    conn = None
    try:
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (username, phone_number, card_number, event_list) VALUES (?, ?, ?, ?)''',
                       (username, phone_number, card_number, '[]'))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while registering the user: {e}")
    finally:
        if conn:
            conn.close()


def get_event_list(user_id):
    conn = None
    try:
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        cursor.execute('''SELECT event_list FROM users WHERE user_id = ?''', (user_id,))
        event_list = cursor.fetchone()
        return event_list
    except sqlite3.Error as e:
        print(f"An error occurred while fetching event list: {e}")
        return None
    finally:
        if conn:
            conn.close()


def add_event(user_id, new_event):
    event_list = json.loads(get_event_list(user_id)[0])
    event_list.append(new_event)
    a = json.dumps(event_list)

    conn = None
    try:
        conn = sqlite3.connect(users_db, timeout=10)
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET event_list = ? WHERE user_id = ?''', (a, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while adding an event: {e}")
    finally:
        if conn:
            conn.close()


def take_id_by_phonenumber(phonenumber):
    conn = None
    try:
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        cursor.execute('''SELECT user_id FROM users WHERE phone_number = ?''', (phonenumber,))
        q = cursor.fetchone()
        return q
    except sqlite3.Error as e:
        print(f"An error occurred while fetching user ID by phone number: {e}")
        return None
    finally:
        if conn:
            conn.close()


def user_login(username):
    conn = None
    try:
        conn = sqlite3.connect(users_db)
        cursor = conn.cursor()
        cursor.execute('''SELECT username FROM users WHERE username = ?''', (username,))
        result = cursor.fetchone()
        return result is not None  # Возвращает True, если пользователь найден, иначе False
    except sqlite3.Error as e:
        print(f"An error occurred while logging in user: {e}")
        return False
    finally:
        if conn:
            conn.close()


create_users_db()
