from pydantic import BaseModel, Field, HttpUrl


class StartGame(BaseModel):
    """Start game request model."""

    white: str = Field(description="White player's name", min_length=2)
    black: str = Field(description="Black player's name", min_length=2)
    round: int = Field(description="Rounds count", ge=1)
    time_control: str = Field(
        description="Time control in seconds",
        pattern=r"^[1-9][0-9]*(?:\+[1-9][0-9]*)?$",
        examples=["900", "900+60"]
    )
    stream_url: HttpUrl = Field(description="Stream from VK")

