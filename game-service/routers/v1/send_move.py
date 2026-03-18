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
    moves = await ChessFacade.get_moves(board)
    for move in moves:
        await ChessFacade.push(str(move))
        await lichess.send_pgn(str(await ChessFacade.load_game()))
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "moves": [str(move) for move in moves]
        }
    )
