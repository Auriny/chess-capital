from chess import IllegalMoveError
from fastapi import FastAPI

from exceptions import (
    GameNotFoundError,
    base_handler,
    game_not_found_handler,
)
from exceptions.base import CapitalChessBaseError
from routers import api_router
from utils.startup import lifespan

app = FastAPI(
    title="Chess Capital Backend",
    lifespan=lifespan, # type: ignore[arg-type]
    exception_handlers={
        GameNotFoundError: game_not_found_handler,
        CapitalChessBaseError: base_handler,
        IllegalMoveError: base_handler,
    }
)

app.include_router(api_router)
