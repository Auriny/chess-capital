from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from utils import ChessFacade

router = APIRouter()

@router.post(path="/send")
async def send_move(
    board: Annotated[list[list[int]], Query(
        description="Chess board in matrix"
    )]
) -> JSONResponse:
    move = await ChessFacade.get_move(board)
    await ChessFacade.push(move)
    return JSONResponse(
        status_code=200,
        content={"status": "ok","move": move}
    )
