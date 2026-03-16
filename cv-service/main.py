import os
from dotenv import dotenv_values
from pathlib import Path

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse


dotenv_path = Path(__file__).parent / ".env"
if not dotenv_path.exists():
    dotenv_path.touch()
    dotenv_path.write_text("SECRET_KEY=\"\"")
    # dotenv_path.write_text("DEBUG=False")
    print("Нужно задать API токен!")

config = {
    **os.environ,
    **dotenv_values(".env"),
}

DEBUG = config.get("DEBUG", "False") == "True"

app = FastAPI()


@app.middleware("http")
async def middleware(request: Request, call_next):
    if not DEBUG:
        if config.get("SECRET_KEY") is None:
            return JSONResponse({"message": "SECRET_KEY not set"})

        auth_header = request.headers.get("Authorization")
        if auth_header is None or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"message": "Authorization header missing"})

        auth_token = auth_header[7:]

        if auth_token != config.get("SECRET_KEY"):
            return JSONResponse(status_code=401, content={"message": "Authorization failed"})

    response = await call_next(request)
    return response


@app.post("/api/v1/cv")
async def api(request: Request):
    frame_raw: bytes = await request.body()

    if not frame_raw:
        return JSONResponse(status_code=400, content={"message": "Board frame not set"})

    # frame = frame_raw.decode("utf-8") # На новый год, не трогать!!!

    #TODO: Подключить реальную нейронку
    board_response = [
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]

    return JSONResponse(status_code=200, content=board_response)


if DEBUG:
    print("Работает в режиме отладки")
    print("Игнорируется апи токен")