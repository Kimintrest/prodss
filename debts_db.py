import sqlite3
from loaderof_db import debts_db
def creare_debts_db():  
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Debts (
                        debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        debtor_id INTEGER,
                        creditor_id INTEGER,
                        amount REAL NOT NULL,
                        is_payed BOOLEAN DEFAULT 0,
                        event_fk INTEGER,
                        comment STRING DEFAULT NULL,
                        FOREIGN KEY(debtor_id) REFERENCES Users(users_id),
                        FOREIGN KEY(creditor_id) REFERENCES Users(users_id),
                        FOREIGN KEY(event_fk) REFERENCES Event(event_id)
                     )''')
    conn.commit()
    conn.close()


def delete_by_id(event_id):
    conn = sqlite3.connect(debts_db)
    cursor = conn.cursor()
    try:   
        cursor.execute("DELETE FROM Debts WHERE debt_id = ?", (event_id))
        conn.commit()
    except Exception:
        return "Что-то пошло не так" 

  

        