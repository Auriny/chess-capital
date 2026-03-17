from fastapi.requests import Request
from fastapi.responses import JSONResponse

from exceptions.game_not_found import GameNotFoundError


async def exc_handler(
    _: Request,
    exc: GameNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "active": exc.active,
            "message": exc.message
        }
    )


__all__ = ("GameNotFoundError", "exc_handler")
