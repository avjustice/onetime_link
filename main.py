import random
import string
import hashlib
from fastapi import FastAPI
from database import conn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/generate")
async def generate(code: str, message: str):
    secret_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    hashed_code = hashlib.sha256(code.encode('utf-8')).hexdigest()
    conn.hset(secret_key, mapping={
        'code': hashed_code,
        'message': message
    })
    return {
        'key': secret_key,
        'link': f'http://127.0.0.1:8000/secrets/{secret_key}?code={code}'
    }


@app.get("/secrets/{secret_key}")
async def secrets(secret_key: str, code: str):
    info_by_secret_key = conn.hgetall(secret_key)
    hashed_code = hashlib.sha256(code.encode('utf-8')).hexdigest()
    if info_by_secret_key.get('code') == hashed_code:
        response = info_by_secret_key.get('message')
        conn.delete(secret_key)
        return response
    elif info_by_secret_key:
        return {'message': 'Code is wrong'}
    return {'message': 'Secret key doesn\'t exist'}
