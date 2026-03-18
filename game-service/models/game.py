from pydantic import BaseModel


class Game(BaseModel):
    """Chess game class."""

    fen: str
    pgn: str
