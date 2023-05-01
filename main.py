import random
import string
import redis
import hashlib
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/generate")
async def generate(code: str, message: str):
    secret_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    hashed_code = hashlib.sha256(code.encode('utf-8')).hexdigest()
    r.hset(secret_key, mapping={
        'code': hashed_code,
        'message': message
    })
    return {"key": secret_key}


@app.get("/secrets/{secret_key}")
async def secrets(secret_key: str, code: str):
    tmp = r.hgetall(secret_key)
    hashed_code = hashlib.sha256(code.encode('utf-8')).hexdigest()
    if tmp.get('code') == hashed_code:
        response = tmp.get('message')
        r.delete(secret_key)
        return response
    return None


@app.get("/meme")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
