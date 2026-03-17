from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from enums.statuses import ResponseStatuses
from utils.chess_facade import ChessFacade

router = APIRouter()

@router.post(path="/send")
async def send_move(
    move: Annotated[str, Query(
        description="Player's move in UCI notation",
        pattern=r"([a-h][1-8]){2}",
        min_length=4, max_length=4
    )]
) -> JSONResponse:
    await ChessFacade.push(move)
    return JSONResponse(
        status_code=200,
        content={"status": ResponseStatuses.OK,"move": move}
    )
