import sqlite3
from loaderof_db import debts_db

def create_debts_db():
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
    conn.close()

def delete_debt_by_id(debt_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debts WHERE debt_id = ?", (debt_id,))
    conn.commit()
    conn.close()

def add_debt(debtor_id, creditor_id, amount, event_fk, is_payed=0):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO debts (debtor_id, creditor_id, amount, is_payed, event_fk) VALUES (?, ?, ?, ?, ?)",
                   (debtor_id, creditor_id, amount, is_payed, event_fk))
    conn.commit()
    conn.close()

def get_debts_by_event_fk(event_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debts WHERE event_fk = ?", (event_id,))
    debts = cursor.fetchall()
    conn.close()
    return debts


def get_debts_by_user_id_event_id(user_id, event_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debts WHERE event_fk = ? AND debtors_id = ?", (event_id, user_id))
    debtor = cursor.fetchall()
    conn.close()
    return debtor



def get_creditors_by_user_id_event_id(user_id, event_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debts WHERE event_fk = ? AND creditors_id = ?", (event_id, user_id))
    debtor = cursor.fetchall()
    conn.close()
    return debtor
