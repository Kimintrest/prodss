from fastapi import FastAPI, Body
from starlette.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, firestore
import uvicorn

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

# Инициализация приложения FastAPI
app = FastAPI()

@app.post("/register")
async def register(request=Body()):
    username = request["username"]
    phonenumber = request["phonenumber"]
    cardnumber = request["cardnumber"]
    
    try:
        # Проверка существования пользователя
        users_ref = db.collection('users').where('phonenumber', '==', phonenumber).get()
        if users_ref:
            return JSONResponse(content={"message": "Такой пользователь уже существует"}, status_code=400)

        # Добавление пользователя в Firestore
        db.collection('users').add({
            'username': username,
            'phonenumber': phonenumber,
            'cardnumber': cardnumber
        })
        return JSONResponse(content={"message": "Пользователь зарегистрирован"}, status_code=201)
    
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/login")
async def login(request=Body()):
    phonenumber = request["phonenumber"]
    
    try:
        user_ref = db.collection('users').where('phonenumber', '==', phonenumber).get()
        if not user_ref:
            return JSONResponse(content={"message": "Пользователь не найден"}, status_code=404)
        
        return JSONResponse(content={"message": "Успешный вход"}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.post("/get_id_by_phonenumber")
async def get_id(request=Body()):
    phonenumber = request["phonenumber"]
    
    try:
        user_ref = db.collection('users').where('phonenumber', '==', phonenumber).get()
        if not user_ref:
            return JSONResponse(content={"message": "Пользователь не найден"}, status_code=404)

        user_id = user_ref[0].id  # Получаем ID пользователя
        return {"user_id": user_id}
    
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

# Остальные функции адаптируйте аналогично, используя Firestore для хранения и получения данных.

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
