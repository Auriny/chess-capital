import os, dotenv

from fastapi import FastAPI

from routers import router as api_router
import config as cfg


config = {
    **os.environ,
    **dotenv.dotenv_values(".env")
}

cfg.GAME_PORT = config["GAME_PORT"]

app = FastAPI()

app.include_router(api_router)