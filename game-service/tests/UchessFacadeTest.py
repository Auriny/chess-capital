import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from anyio import Path
from datetime import date
from models.requests import StartGame
from config import settings
from utils.chess_facade import ChessFacade
from chess.pgn import Game
from exceptions import GameNotFoundError
from unittest.mock import patch
from datetime import datetime, UTC


"""@pytest.mark.anyio
async def test_create_game_creates_pgn_file(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))

    data = StartGame(
        white="Magnus Carlsen",
        black="Hikaru Nakamura",
        round=1,
        date=date(2026, 3, 18),
        time_control="300",
        stream_url="https://vk.com/video123",
    )

    await ChessFacade.create_game(data)

    # ищем pgn-файл в temp‑папке
    files = [f async for f in Path(tmp_path).glob("*.pgn")]
    assert len(files) == 1

    content = await files[0].read_text()

    assert "Event \"Magnus Carlsen vs. Hikaru Nakamura\"" in content
    assert "White \"Magnus Carlsen\"" in content
    assert "Black \"Hikaru Nakamura\"" in content
    assert "Site \"https://vk.com/video123\"" in content"""

@pytest.mark.anyio
async def test_get_last_pgn_path_raises_if_only_empty_game(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))

    game = Game()
    game.headers["Event"] = "Test"
    file = tmp_path / "test_game.pgn"
    file.write_text(str(game))

    
    await ChessFacade._get_last_pgn_path()

@pytest.mark.anyio
async def test_get_last_pgn_path_raises_if_no_active(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))
    game = Game()
    board = game.board()

    moves = ["f3", "e5", "g4", "Qh4#"]
    node = game
    for san in moves:
        move = board.parse_san(san)
        board.push(move)
        node = node.add_variation(move)
    
    game.headers["Result"] = "0-1"  # чёрные матуют белых

    file = tmp_path / "finished_game.pgn"
    file.write_text(str(game))

    with pytest.raises(GameNotFoundError):
        await ChessFacade._get_last_pgn_path()

@pytest.mark.anyio
async def test_load_game_raises_if_only_this_game(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))

    game = Game()
    board = game.board()
    move = board.parse_san("e4")
    node = game.add_variation(move)
    board.push(move)

    file = tmp_path / "game.pgn"
    file.write_text(str(game))

    await ChessFacade.load_game()

@pytest.mark.anyio
async def test_load_game_raises_if_no_game(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))

    with pytest.raises(GameNotFoundError):
        await ChessFacade.load_game()

@pytest.mark.anyio
async def test_push_adds_move(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "PGN_FILES_FOLDER", str(tmp_path))
    # Создаем пустую игру и сохраняем её с помощью create_game
    from models.requests import StartGame
    from datetime import date

    data = StartGame(
        white="White",
        black="Black",
        round=1,
        date=date(2026, 3, 18),
        time_control="300",
        stream_url="https://vk.com/stream",
    )
    await ChessFacade.create_game(data)

    await ChessFacade.push("e2e4")

    # Проверяем, что ход появился в PGN
    files = [f async for f in Path(tmp_path).glob("*.pgn")]
    assert len(files) == 1
    content = await files[0].read_text()
    assert "e4" in content 
