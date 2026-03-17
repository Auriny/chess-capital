from chess import IllegalMoveError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from exceptions.game_not_found import GameNotFoundError


async def game_not_found_handler(
    _: Request,
    exc: GameNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=200, content={"active": exc.active, "message": exc.message}
    )

async def illegal_move_handler(
    _: Request,
    exc: IllegalMoveError
) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"details": exc.args}
    )
