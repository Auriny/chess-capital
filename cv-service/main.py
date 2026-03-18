import os, dotenv

from fastapi import FastAPI

from routers.frame import router as frame_router
import config as cfg


config = {
    **os.environ,
    **dotenv.dotenv_values(".env")
}

cfg.GAME_PORT = config["GAME_PORT"]
cfg.HOST_NAME = config["HOST_NAME"]

app = FastAPI()

app.include_router(frame_router)