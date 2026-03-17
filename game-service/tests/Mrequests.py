import pytest
import os
import sys
from pydantic import HttpUrl

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from datetime import date
from models.requests import StartGame

def test_start_game_model_validation():
    """Проверяем валидацию Pydantic модели напрямую."""
    # Валидная модель
    game = StartGame(
        white="AlphaZero",
        black="Stockfish", 
        round=5,
        date=date(2026, 3, 17),
        time_control="900",
        stream_url="https://vk.com/chess_stream"
    )
    assert game.white == "AlphaZero"
    assert game.round == 5
    assert game.stream_url == HttpUrl("https://vk.com/chess_stream")

def test_start_game_model_invalid_round():
    """Тест ошибки валидации round."""
    with pytest.raises(ValueError):
        StartGame(
            white="Player1",
            black="Player2",
            round=0,  # ge=1
            date=date(2026, 3, 17),
            time_control="300",
            stream_url="https://example.com"
        )