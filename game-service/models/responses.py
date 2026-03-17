from pydantic import BaseModel

from models.game import Game


class GameResponse(BaseModel):
    """Game response class."""

    active: bool
    game: Game
    stream_url: str
