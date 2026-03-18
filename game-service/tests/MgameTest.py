import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from pydantic import ValidationError
from models.game import Game


def test_game_valid_creation():
    """Модель создаётся с валидными строками fen/pgn."""
    g = Game(
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        pgn="1. e4 e5 2. Nf3 Nc6"
    )
    assert g.fen.startswith("rnbqkbnr")
    assert "e4" in g.pgn


def test_game_model_dump():
    """Проверяем сериализацию в dict."""
    g = Game(
        fen="startpos",
        pgn="1. d4 d5"
    )
    data = g.model_dump()
    assert data == {
        "fen": "startpos",
        "pgn": "1. d4 d5"
    }


def test_game_rejects_non_string_fen():
    """fen не принимает int — ожидаем ValidationError."""
    with pytest.raises(ValidationError):
        Game(
            fen=12345,          # int → ошибка
            pgn="1. e4"
        )

def test_game_missing_field_fen():
    """Отсутствующее поле fen должно вызвать ValidationError."""
    with pytest.raises(ValidationError):
        Game(pgn="1. e4")   # fen не передан


def test_game_missing_field_pgn():
    """Отсутствующее поле pgn должно вызвать ValidationError."""
    with pytest.raises(ValidationError):
        Game(fen="startpos")  # pgn не передан
