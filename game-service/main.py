from fastapi import FastAPI

from exceptions import GameNotFoundError, exc_handler
from routers import api_router
from utils.startup import check_pgn_folder

app = FastAPI(
    title="Chess Capital Backend",
    on_startup=check_pgn_folder(),
    exception_handlers={GameNotFoundError: exc_handler}
)

app.include_router(api_router)
