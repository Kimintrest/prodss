import sqlite3
from loaderof_db import users_db
def create_users_db():
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        phone_number NOT NULL,
                        card_number DEFAULT NULL
                     )''')
    conn.commit()
    conn.close()


def user_register(username, phone_number, card_number=None):
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO Users (username, phone_number, card_number)
                          VALUES (?, ?, ?, ?)''', (username, phone_number, card_number))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def user_login(username):
    conn = sqlite3.connect(users_db)
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT username FROM Users WHERE username = ?''', (username))
    except Exception:
        return "Пользователь с таким ником уже существует"
    conn.close()

create_users_db()