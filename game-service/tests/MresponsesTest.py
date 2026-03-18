import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from urllib.parse import urlparse
from pydantic import ValidationError
from models.responses import GameResponse  # импорт твоей модели
from models.game import Game  # предполагаемая модель
from pydantic import HttpUrl

class TestGameResponse:
    
    def test_valid_game_response(self):
        """Валидная GameResponse с корректными данными."""
        # Мок Game (замени на реальную структуру твоего Game)
        mock_game = Game(
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            pgn="1. e4"
        )
        
        game_response = GameResponse(
            active=True,
            game=mock_game,
            stream_url="https://vk.com/video123456"
        )
        
        # Проверяем значения
        assert game_response.active is True
        assert game_response.game.fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        assert str(game_response.stream_url) == "https://vk.com/video123456"
    
    def test_invalid_stream_url(self):
        """Невалидный HttpUrl — ValidationError."""
        mock_game = Game(fen="startpos", pgn="1. e4")
        
        with pytest.raises(ValidationError):
            GameResponse(
                active=True,
                game=mock_game,
                stream_url="not-a-valid-url"  # ❌ не HttpUrl
            )
    
    def test_invalid_active_type(self):
        """active должен быть bool."""
        mock_game = Game(fen="startpos", pgn="1. e4")
        
        with pytest.raises(ValidationError):
            GameResponse(
                active="not_bool",  # ❌ str вместо bool
                game=mock_game,
                stream_url="https://vk.com/video"
            )
    
    def test_model_dump(self):
        """Проверяем model_dump() для JSON сериализации."""
        mock_game = Game(fen="rnbqkbnr/pppppppp/8/8/4P3/8/PPP1PPPP/RNBQKBNR b KQkq - 1 1", pgn="1. e4")
        
        game_response = GameResponse(
            active=False,
            game=mock_game,
            stream_url="https://vk.com/chess_stream"
        )
        
        dumped = game_response.model_dump()
        assert dumped["active"] is False
        assert dumped["game"]["fen"] == "rnbqkbnr/pppppppp/8/8/4P3/8/PPP1PPPP/RNBQKBNR b KQkq - 1 1"
        assert dumped["stream_url"] == HttpUrl("https://vk.com/chess_stream")
    
    def test_from_api_response(self):
        """Тест создания из типичного API ответа (как в game_process.py)."""
        api_data = {
            "active": True,
            "game": {
                "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPP1PPPP/RNBQKBNR b KQkq - 1 1",
                "pgn": "1. e4 e5"
            },
            "stream_url": "https://vk.com/video987654"
        }
        
        # Pydantic автоматически парсит в GameResponse
        game_response = GameResponse.model_validate(api_data)
        assert game_response.active is True
        assert game_response.stream_url == HttpUrl("https://vk.com/video987654")

    def test_httpurl_normalization(self):
        """HttpUrl нормализует URL (убирает слеши, делает lowercase)."""
        mock_game = Game(fen="startpos", pgn="")
        
        game_response = GameResponse(
            active=True,
            game=mock_game,
            stream_url="HTTPs://VK.COM/video123///extra//"
        )
        
        # Pydantic HttpUrl: lowercase + scheme, слеши остаются
        assert str(game_response.stream_url) == "https://vk.com/video123///extra//"
    
         # Проверяем только схему и хост
        parsed = urlparse(str(game_response.stream_url))
        assert parsed.scheme == "https"
        assert parsed.netloc == "vk.com"
        assert parsed.path == "/video123///extra//"
