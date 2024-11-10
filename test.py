import time

import requests
import json

# URL вашего FastAPI приложения
BASE_URL = "http://localhost:5000"  # или другой URL, если приложение работает не на localhost

# Test POST /register
def test_register():
    url = f"{BASE_URL}/register"
    data = {
        "username": "testuser",
        "phonenumber": "1234567890",
        "cardnumber": "1234-5678-9012-3456"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.text != "Такой пользователь уже существует или что-то пошло не так"



# Test POST /login
def test_login():
    time.sleep(1)
    url = f"{BASE_URL}/login"
    data = {
        "phonenumber": "1234567890"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.text != "Такой пользователь уже существует"

# Test POST /get_id_by_phonenumber
def test_get_id_by_phonenumber():
    url = f"{BASE_URL}/get_id_by_phonenumber"
    data = {
        "phonenumber": "1234567890"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert  type(response.json()) == int  # ожидаем, что id будет в ответе

def test_create_event():
    url = f"{BASE_URL}/create_event"
    data = {
        "name": "Test Event",
        "user_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

def test_add_event():
    url = f"{BASE_URL}/add_event"
    data = {
        "user_id": 1,
        "unique_code": "4598317"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
#
# Test POST /optimize_graph
def test_optimize_graph():
    url = f"{BASE_URL}/optimize_graph"
    data = {
        "event_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200

# Test POST /get_debtors
def test_get_debtors():
    url = f"{BASE_URL}/get_debtors"
    data = {
        "user_id": "1",
        "event_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'debtors' in response.json()

# Test POST /get_creditors
def test_get_creditors():
    url = f"{BASE_URL}/get_creditors"
    data = {
        "user_id": "1",
        "event_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'creditors' in response.json()

# Test POST /get_event_by_uniquecode
def test_get_event_by_uniquecode():
    url = f"{BASE_URL}/get_event_by_uniquecode"
    data = {
        "unique_code": "593585"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    event_data = response.json()
    assert 'event_id' in event_data
    assert 'name' in event_data
    assert 'status' in event_data
    assert 'admin' in event_data
    assert 'unique_code' in event_data
    assert 'users_list' in event_data

# Test POST /get_event_list
def test_get_event_list():
    url = f"{BASE_URL}/get_event_list"
    data = {
        "user_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'events' in response.json()

# Test POST /add_event


# Test POST /create_event


# Test POST /create_transfer
def test_create_transfer():
    url = f"{BASE_URL}/create_transfer"
    data = {
        "creditor_id": "1",
        "debtor_id": "2",
        "amount": 100.0,
        "event_id": "1"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    # Here, check if the debt is properly added by fetching from the database or checking responses