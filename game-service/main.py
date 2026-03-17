from chess import IllegalMoveError
from fastapi import FastAPI

from exceptions import (
    GameNotFoundError,
    game_not_found_handler,
    illegal_move_handler,
)
from routers import api_router
from utils.startup import lifespan

app = FastAPI(
    title="Chess Capital Backend",
    lifespan=lifespan, # type: ignore[arg-type]
    exception_handlers={
        GameNotFoundError: game_not_found_handler,
        IllegalMoveError: illegal_move_handler,
    }
)

app.include_router(api_router)
