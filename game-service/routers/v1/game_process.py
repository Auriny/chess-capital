from typing import Annotated

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from models.requests import StartGame
from models.responses import GameResponse
from utils.chess_facade import ChessFacade

router = APIRouter()

@router.post("/start")
async def start_game(body: Annotated[StartGame, Body(
    description="Game settings"
)]) -> JSONResponse:
    await ChessFacade.create_game(body)
    return JSONResponse(
        status_code=200,
        content={"active": True}
    )

@router.get("/data")
async def get_game_data() -> JSONResponse:
    game = await ChessFacade.load_game()
    return JSONResponse(
        status_code=200,
        content=GameResponse(
            active=True,
            game={
                "fen": game.end().board().fen(),
                "pgn": str(game)
            },
            stream_url=game.headers["Site"]
        ).model_dump(mode="json")
    )

@router.post("/end")
async def end_game() -> JSONResponse:
    await ChessFacade.end_game()
    return JSONResponse(
        status_code=200,
        content={"status": "ok"}
    )
