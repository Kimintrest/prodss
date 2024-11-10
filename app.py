from fastapi import FastAPI
import datetime, random, uvicorn, string, time
from fastapi import FastAPI, Body, File, UploadFile, Form
from starlette.responses import JSONResponse
import threading
from fastapi.middleware.cors import CORSMiddleware
import json
import debts_db
import users_db
import event_db
import utils



# Initialise the app
app = FastAPI()


@app.post("/register")
async def register(request=Body()):
    username = request["username"]
    phonenumber = request["phonenumber"]
    cardnumber = request["cardnumber"]
    try:
        users_db.user_register(username, phonenumber, cardnumber)
    except Exception:
        return "Такой пользователь уже существует или что-то пошло не так"


@app.post("/login")
async def login(request=Body()):
    phonenumber = request["phonenumber"]
    try:
        users_db.user_login(phonenumber)
    except Exception:
        return "Такой пользователь уже существует"


@app.post("/get_id_by_phonenumber")
async def get_id(request=Body()):
    phonenumber = request["phonenumber"]
    # try:
    q = users_db.take_id_by_phonenumber(phonenumber)
    print(q)
    return q[0]
    # except Exception:
    #     return "Что-то пошло не так"

# return JSONResponse({'message': 'Товар сохранен'}, status_code=200)
# return JSONResponse({'error': 'Данные не были сохранены, повторите отправку'}, status_code=404)
#


@app.post('/optimize_graph')
async def save_item(request=Body()):
    event_id = request['event_id']
    if event_db.get_admin_by_event_id(event_id) == int(event_id):
        debts = debts_db.get_debts_by_event_fk(event_id)
        o_debts = [(debt[2], debt[1], debt[3]) for debt in debts]
        optimize_debts = utils.optimize(o_debts)
        for del_debt in debts:
            debts_db.delete_debt_by_id(del_debt[0])
        for all_debt in optimize_debts:
            debts_db.add_debt(all_debt[1], all_debt[0],all_debt[2], event_id)
        event_db.update_event_status_by_uniquecode(event_id, 1)



@app.post('/get_debtors')
async def get_debtor(request=Body()):
    user_id = request['user_id']
    event_id = request['event_id']
    debtors = debts_db.get_debts_by_user_id_event_id(user_id, event_id)
    return {'debtors': debtors if debtors else None}


@app.post('/get_creditors')
async def get_creditor(request=Body()):
    user_id = request['user_id']
    event_id = request['event_id']
    creditors = debts_db.get_creditors_by_user_id_event_id(user_id, event_id)
    return {'creditors': creditors if creditors else None}


@app.post('/get_event_by_uniquecode')
async def get_object_of_event(request=Body()):
    unique_code = request["unique_code"]
    lst = list(event_db.get_event_by_uniquecode(unique_code))

    return {"event_id": lst[0], "name": lst[1], "status": lst[2], "admin": lst[3],
            "unique_code": lst[4], "users_list": lst[5]}


@app.post('/get_event_list')
async def get_event_list(request=Body()):
    user_id = request['user_id']
    return {'events': users_db.get_event_list(user_id)}
import asyncio

@app.post('/add_event')
async def add_event(request=Body()):
    user_id = request['user_id']
    unique_code = request['unique_code']
    print(user_id, unique_code)

    users_db.add_event(user_id, unique_code)


@app.post("/create_event")
async def creation_of_event(request=Body()):
    name = request["name"]
    user_id = request["user_id"]
    event_db.add_event(name, user_id)
    return "Вы успешно создали событие"

@app.post('/create_transfer')
async def create_transfer(request=Body()):
    creditor_id = request['creditor_id']
    debtor_id = request['debtor_id']
    amount = request['amount']
    event_id = request['event_id']
    debts_db.add_debt(debtor_id, creditor_id, amount, event_id)














if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

