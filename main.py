import random
import string

from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()
MY_DICT = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/generate")
async def generate(code: str, message: str):
    secret_key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    MY_DICT[secret_key] = {
        'code': code,
        'message': message
    }
    return {"key": secret_key}


@app.get("/secrets/{secret_key}")
async def say_hello(secret_key: str, code: str):
    if secret_key in MY_DICT and MY_DICT[secret_key]['code'] == code:
        response = MY_DICT[secret_key]['message']
        del MY_DICT[secret_key]
        return response
    return {"message": "key not found or code is bad"}


@app.get("/meme")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
