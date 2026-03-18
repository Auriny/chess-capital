import asyncio
import io
from datetime import UTC, datetime

from anyio import Path, to_thread
from chess import WHITE, Board, IllegalMoveError, Move, square
from chess.pgn import Game, read_game

from config import settings
from exceptions import (
    GameNotFoundError,
    InvalidBoardMatrixError,
    TooManyMovesError,
)
from models.requests import StartGame
from utils.lichess_stream import lichess


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
            if game and (
                game.headers["Result"] == "*"
                or not file.name.startswith("FINISHED_")
            ):
                if game.headers["Result"] != "*":
                    file = await file.rename(  # noqa: PLW2901
                        f"{settings.PGN_FILES_FOLDER}/FINISHED_{file.name}"
                    )
                return file
        msg = "No active games found."
        raise GameNotFoundError(active=False, msg=msg)

    @staticmethod
    async def create_game(data: StartGame) -> None:
        game = Game()
        dt = datetime.now(tz=UTC)
        game.headers.update({
            "Event": f"{data.white} vs. {data.black}",
            "White": data.white,
            "Black": data.black,
            "Date": str(dt.date()),
            "TimeControl": str(data.time_control),
            "Round": str(data.round),
            "Site": str(data.stream_url),
        })
        formated_dt = dt.strftime("%Y%m%d_%H%M%S")
        file = Path(
            f"{settings.PGN_FILES_FOLDER}/{formated_dt}.pgn"
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
        game_str = str(game)
        await pgn.write_text(game_str)

    @staticmethod
    async def push(move: str) -> None:
        game = await ChessFacade.load_game()
        node = game.end()
        move_instance = Move.from_uci(move)
        if move_instance not in node.board().legal_moves:
            msg = f"Illegal move {move!s}"
            raise IllegalMoveError(msg)
        node.add_variation(move_instance)
        if (game.end().board().is_game_over()):
            game.headers["Result"] = game.end().board().result()
        await ChessFacade.save_game(game)

    @staticmethod
    async def end_game() -> None:
        game = await ChessFacade.load_game()
        game.headers["Result"] = "1/2-1/2"
        await lichess.send_pgn(str(game.end()))
        await lichess.end()
        await ChessFacade.save_game(game)

    @staticmethod
    def board_to_matrix(board: Board) -> list[list[int]]:
        result = []
        for rank in range(7, -1, -1):
            row = []
            for file in range(8):
                piece = board.piece_at(square(file, rank))
                row.append(
                    0 if piece is None else (1 if piece.color == WHITE else 2)
                )
            result.append(row)
        return result

    @staticmethod
    def matrix_to_frozenset(
        matrix: list[list[int]],
    ) -> frozenset[tuple[int, int]]:
        occupied = set()
        for r, row in enumerate(matrix):
            for f, val in enumerate(row):
                if val != 0:
                    occupied.add((square(f, 7 - r), val))
        return frozenset(occupied)

    @staticmethod
    def validate_matrix(matrix: list[list[int]]) -> bool:
        if len(matrix) != 8 or any(len(row) != 8 for row in matrix):  # noqa: PLR2004
            return False
        white = sum(v == 1 for row in matrix for v in row)
        black = sum(v == 2 for row in matrix for v in row)  # noqa: PLR2004
        return (
            all(v in (0, 1, 2) for row in matrix for v in row)
            and 1 <= white <= 16  # noqa: PLR2004
            and 1 <= black <= 16  # noqa: PLR2004
        )

    @staticmethod
    def find_moves(
        board: Board, target: frozenset, depth: int = 2
    ) -> list[Move]:
        for move in board.legal_moves:
            board.push(move)
            if ChessFacade.matrix_to_frozenset(
                ChessFacade.board_to_matrix(board)
            ) == target:
                board.pop()
                return [move]
            if depth > 1:
                for move2 in board.legal_moves:
                    board.push(move2)
                    if ChessFacade.matrix_to_frozenset(
                        ChessFacade.board_to_matrix(board)
                    ) == target:
                        board.pop()
                        board.pop()
                        return [move, move2]
                    board.pop()
            board.pop()
        msg = "Too many movess for processing"
        raise TooManyMovesError(msg)

    @staticmethod
    async def get_moves(matrix: list[list[int]]) -> list[Move]:
        if not ChessFacade.validate_matrix(matrix):
            msg = "Invalid matrix"
            raise InvalidBoardMatrixError(msg)
        board = (await ChessFacade.load_game()).end().board()
        target = ChessFacade.matrix_to_frozenset(matrix)
        if ChessFacade.matrix_to_frozenset(
            ChessFacade.board_to_matrix(board)
        ) == target:
            return []
        return await asyncio.to_thread(ChessFacade.find_moves, board, target)
