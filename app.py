from fastapi import FastAPI
import datetime, random, uvicorn, string, time
from fastapi import FastAPI, Body, File, UploadFile, Form
from starlette.responses import JSONResponse
import threading
from fastapi.middleware.cors import CORSMiddleware
import json
import debts_db
import event_db
from . import utils

SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"

# encryption algorithm
ALGORITHM = "HS256"


# Pydantic Model that will be used in the
# token endpoint for the response
class Token():
    access_token: str
    token_type: str


# Initialise the app
app = FastAPI()


# this function will create the token
# for particular data
# def create_access_token(data: dict):
#     to_encode = data.copy()
#
#     # expire time of the token
#     expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#     # return the generated token
#     return encoded_jwt


# return JSONResponse({'message': 'Товар сохранен'}, status_code=200)
# return JSONResponse({'error': 'Данные не были сохранены, повторите отправку'}, status_code=404)
#


@app.post('/optimize_graph')
async def save_item(request=Body()):
    event_id = request['event_id']
    if event_db.get_admin_by_event_id(event_id) == event_id:
        debts = debts_db.get_debts_by_event_fk(event_id)
        o_debts = [(debt[2], debt[1], debt[3]) for debt in debts]
        optimize_debts = utils.optimize(o_debts)
        for del_debt in debts:
            debts_db.delete_debt_by_id(del_debt[0])
        for all_debt in optimize_debts:
            debts_db.add_debt(all_debt[1], all_debt[0],all_debt[2], event_id)


@app.post('/get_event_by_uniquecode')
async def get_object_of_event(request=Body()):
    unique_code = request["unique_code"]
    return json.loads(event_db.get_event_by_uniquecode(unique_code))



@app.post('/get_debtors')
async def get_debtor(request=Body()):
    user_id = request['user_id']
    event_id = request['event_id']

    return {'debtors': json.loads(debts_db.get_debts_by_user_id_event_id(user_id, event_id))}


@app.post('/get_creditors')
async def get_creditor(request=Body()):
    user_id = request['user_id']
    event_id = request['event_id']

    return {'debtors': json.loads(debts_db.get_creditors_by_user_id_event_id(user_id, event_id))}


@app.post('/reg')
async def reg(request=Body()):




@app.post('/create_session')
async def save_item(request=Body()):



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
