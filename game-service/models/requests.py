import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator


class StartGame(BaseModel):
    """Start game request model."""

    white: str = Field(description="White player's name", min_length=2)
    black: str = Field(description="Black player's name", min_length=2)
    round: int = Field(description="Rounds count", ge=1)
    date: datetime.date = Field(description="Game's datetime")
    time_control: str = Field(
        description="Time control in seconds",
        pattern=r"^[1-9][0-9]*(?:\+[1-9][0-9]*)?$"
    )
    stream_url: HttpUrl = Field(description="Stream from VK")

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: datetime.date) -> datetime.date:
        if value < datetime.datetime.now(tz=datetime.UTC).date():
            msg = "Date must be today or later."
            raise ValueError(msg)
        return value

