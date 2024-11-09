from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import hashlib
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

