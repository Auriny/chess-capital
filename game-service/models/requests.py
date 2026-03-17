import datetime

from pydantic import BaseModel, Field, HttpUrl


class StartGame(BaseModel):
    """Start game request model."""

    white: str = Field(description="White player's name")
    black: str = Field(description="Black player's name")
    round: int = Field(description="Rounds count")
    date: datetime.date = Field(description="Game's datetime")
    time_control: int = Field(description="Time control in seconds")
    stream_url: HttpUrl = Field(description="Stream from VK")
