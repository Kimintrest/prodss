import json
import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

def create_users_db():
    # Firestore автоматически создает коллекции при добавлении документов,
    # поэтому здесь нет необходимости явно создавать базу данных.
    pass

def user_register(username, phone_number, card_number=None):
    user_data = {
        "username": username,
        "phone_number": phone_number,
        "card_number": card_number,
        "event_list": []
    }
    
    try:
        db.collection('users').add(user_data)
        print("User registered successfully.")
    except Exception as e:
        print(f"Error: {e}")

def get_event_list(user_id):
    try:
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            return user_doc.to_dict().get('event_list', [])
        else:
            print("User not found.")
            return []
    except Exception as e:
        print(f"Error fetching event list: {e}")
        return []

def add_event(user_id, new_event):
    event_list = get_event_list(user_id)
    event_list.append(new_event)
    
    try:
        user_ref = db.collection('users').document(user_id)
        user_ref.update({"event_list": event_list})
    except Exception as e:
        print(f"Error updating event list: {e}")

def take_id_by_phonenumber(phone_number):
    try:
        users_ref = db.collection('users')
        query = users_ref.where('phone_number', '==', phone_number).limit(1).get()
        
        if query:
            return query[0].id  # Возвращаем ID первого найденного пользователя
        else:
            print("User not found.")
            return None
    except Exception as e:
        print(f"Error fetching user by phone number: {e}")
        return None

def user_login(username):
    try:
        users_ref = db.collection('users')
        query = users_ref.where('username', '==', username).limit(1).get()
        
        if query:
            return "User logged in successfully."
        else:
            return "User not found."
    except Exception as e:
        print(f"Error during login: {e}")
        return "An error occurred."

create_users_db()
