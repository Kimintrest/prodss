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
                        event_fk INTEGER,
                        comment TEXT DEFAULT NULL
                     )''')
    conn.commit()
    conn.close()

def delete_debt_by_id(debt_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM debts WHERE debt_id = ?", (debt_id,))
    conn.commit()
    conn.close()

def add_debt(debtor_id, creditor_id, amount, event_fk, comment, is_payed=0):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO debts (debtor_id, creditor_id, amount, is_payed, event_fk, comment) VALUES (?, ?, ?, ?, ?, ?)",
                   (debtor_id, creditor_id, amount, is_payed, event_fk, comment))
    conn.commit()
    conn.close()

def get_debts_by_event_fk(event_fk):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM debts WHERE event_fk = ?", (event_fk,))
    debts = cursor.fetchall()
    conn.close()
    return debts
