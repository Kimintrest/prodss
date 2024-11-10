import sqlite3
from loaderof_db import debts_db


def create_debts_db():
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS debts (
                            debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            debtor_id INTEGER,
                            creditor_id INTEGER,
                            amount REAL NOT NULL,
                            is_payed BOOLEAN DEFAULT 0,
                            event_fk INTEGER
                         )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
def delete_debt_by_id(debt_id):
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM debts WHERE debt_id = ?", (debt_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def add_debt(debtor_id, creditor_id, amount, event_fk, is_payed=0):
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO debts (debtor_id, creditor_id, amount, is_payed, event_fk) VALUES (?, ?, ?, ?, ?)",
                       (debtor_id, creditor_id, amount, is_payed, event_fk))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

def get_debts_by_event_fk(event_id):
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM debts WHERE event_fk = ?", (event_id,))
        debts = cursor.fetchall()
        return debts
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_debts_by_user_id_event_id(user_id, event_id):
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM debts WHERE event_fk = ? AND debtor_id = ?", (event_id, user_id))
        debtor = cursor.fetchall()
        return debtor
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_creditors_by_user_id_event_id(user_id, event_id):
    conn = None
    try:
        conn = sqlite3.connect(debts_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM debts WHERE event_fk = ? AND creditor_id = ?", (event_id, user_id))
        creditor = cursor.fetchall()
        return creditor
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if conn:
            conn.close()
