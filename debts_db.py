import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

def create_debts_collection():
    # Firestore автоматически создает коллекцию при добавлении документа, 
    # поэтому здесь нет необходимости явно создавать коллекцию.
    pass

def delete_debt_by_id(debt_id):
    try:
        db.collection('debts').document(debt_id).delete()
        print(f"Долг с ID {debt_id} успешно удален.")
    except Exception as e:
        print(f"Ошибка при удалении долга: {str(e)}")

def add_debt(debtor_id, creditor_id, amount, event_fk, is_payed=0):
    try:
        debt_data = {
            'debtor_id': debtor_id,
            'creditor_id': creditor_id,
            'amount': amount,
            'is_payed': is_payed,
            'event_fk': event_fk
        }
        db.collection('debts').add(debt_data)
        print("Долг успешно добавлен.")
    except Exception as e:
        print(f"Ошибка при добавлении долга: {str(e)}")

def get_debts_by_event_fk(event_id):
    try:
        debts_ref = db.collection('debts').where('event_fk', '==', event_id).stream()
        debts = [debt.to_dict() for debt in debts_ref]
        return debts
    except Exception as e:
        print(f"Ошибка при получении долгов: {str(e)}")
        return []

def get_debts_by_user_id_event_id(user_id, event_id):
    try:
        debts_ref = db.collection('debts').where('event_fk', '==', event_id).where('debtor_id', '==', user_id).stream()
        debtor = [debt.to_dict() for debt in debts_ref]
        return debtor
    except Exception as e:
        print(f"Ошибка при получении долгов по пользователю: {str(e)}")
        return []

def get_creditors_by_user_id_event_id(user_id, event_id):
    try:
        creditors_ref = db.collection('debts').where('event_fk', '==', event_id).where('creditor_id', '==', user_id).stream()
        creditor = [debt.to_dict() for debt in creditors_ref]
        return creditor
    except Exception as e:
        print(f"Ошибка при получении кредиторов: {str(e)}")
        return []

create_debts_collection()
