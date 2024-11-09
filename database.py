import sqlite3

# Создание базы данных и таблиц
def create_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Session (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                     )''')
                     
    cursor.execute('''CREATE TABLE IF NOT EXISTS Event (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        time_created TEXT DEFAULT CURRENT_TIMESTAMP,
                        session_fk INTEGER,
                        FOREIGN KEY(session_fk) REFERENCES Session(id)
                     )''')
                     
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL
                     )''')
                     
    cursor.execute('''CREATE TABLE IF NOT EXISTS Debts (
                        debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        debtor_id INTEGER,
                        creditor_id INTEGER,
                        amount REAL NOT NULL,
                        is_payed BOOLEAN DEFAULT 0,
                        event_fk INTEGER,
                        time_created TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(debtor_id) REFERENCES Users(users_id),
                        FOREIGN KEY(creditor_id) REFERENCES Users(users_id),
                        FOREIGN KEY(event_fk) REFERENCES Event(event_id)
                     )''')
                     
    conn.commit()
    conn.close()
    
create_db()
