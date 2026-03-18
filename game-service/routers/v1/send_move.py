from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from utils import ChessFacade, lichess

router = APIRouter()

@router.post(path="/send")
async def send_move(
    board: Annotated[list[list[int]], Body(
        description="Chess board in matrix"
    )]
) -> JSONResponse:
    move = await ChessFacade.get_move(board)
    await ChessFacade.push(str(move))
    await lichess.send_pgn(str(ChessFacade.load_game()))
    return JSONResponse(
        status_code=200,
        content={"status": "ok","move": move}
    )
