class LichessStream:
    """Lichess stream class."""

    tournament_id: str
    tournament_name: str

    async def start(self) -> None:
        ...

    async def send_pgn(self, pgn: str) -> None:
        ...

    async def end(self) -> None:
        ...


lichess = LichessStream()
