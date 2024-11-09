from fastapi import FastAPI
import datetime, random, uvicorn, string, time
from fastapi import FastAPI, Body, File, UploadFile, Form
from starlette.responses import JSONResponse
import threading
from fastapi.middleware.cors import CORSMiddleware
import json
import debts_db

SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"

# encryption algorithm
ALGORITHM = "HS256"


# Pydantic Model that will be used in the
# token endpoint for the response
class Token(BaseModel):
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

    debts_db.get_debts_by_event_fk()





@app.post('/get_debitor')
async def get_creditor(request=Body()):


@app.post('/get_debitor')
async def get_creditor(request=Body()):


@app.post('/reg')
async def reg(request=Body()):




@app.post('/create_session')
async def save_item(request=Body()):








if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

