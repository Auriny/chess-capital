import io
from datetime import UTC, datetime

from anyio import Path, to_thread
from chess import Move
from chess.pgn import Game, read_game

from config import settings
from exceptions import GameNotFoundError
from models.requests import StartGame


class ChessFacade:
    """Facade for chess manipulation."""

    @staticmethod
    async def _get_last_pgn_path() -> Path:
        pgn_folder = Path(settings.PGN_FILES_FOLDER)
        files = [i async for i in pgn_folder.glob("*.pgn")]
        files.sort(reverse=True)
        for file in files:
            content = await file.read_text()
            game = await to_thread.run_sync(read_game, io.StringIO(content))
            if (game and not game.end().is_end()):
                return file
        msg = "No active games found."
        raise GameNotFoundError(active=False, msg=msg)

    @staticmethod
    async def create_game(data: StartGame) -> None:
        game = Game()
        game.headers.update({
            "Event": f"{data.white} vs. {data.black}",
            "White": data.white,
            "Black": data.black,
            "Date": str(data.date),
            "TimeControl": str(data.time_control),
            "Round": str(data.round),
            "Site": str(data.stream_url),
        })
        date_and_time = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M:%S%z")
        file = Path(
            f"{settings.PGN_FILES_FOLDER}/{date_and_time}.pgn"
        )
        await file.write_text(str(game))

    @staticmethod
    async def load_game() -> Game:
        pgn = await ChessFacade._get_last_pgn_path()
        content = await pgn.read_text()
        game = await to_thread.run_sync(read_game, io.StringIO(content))
        if game:
            return game
        msg = "No active games found."
        raise GameNotFoundError(active=False, msg=msg)

    @staticmethod
    async def save_game(game: Game) -> None:
        pgn = await ChessFacade._get_last_pgn_path()
        game_str = await to_thread.run_sync(str, game)
        await pgn.write_text(game_str)

    @staticmethod
    async def push(move: str) -> None:
        game = await ChessFacade.load_game()
        node = game.end()
        move_instance = Move.from_uci(move)
        await to_thread.run_sync(node.add_variation, move_instance)
        if (game.end().board().is_game_over()):
            game.headers["Result"] = game.end().board().result()
        await ChessFacade.save_game(game)

    @staticmethod
    async def end_game() -> None:
        game = await ChessFacade.load_game()
        game.headers["Result"] = "1/2-1/2"
        await ChessFacade.save_game(game)
