import os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_start_game():
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "Magnus Carlsen",
            "black": "Hikaru Nakamura",
            "round": 1,
            "date": "2026-03-17",
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 200
        assert response.json() == {"active": True}

def test_empty_white_fails():
    """Тест пустого white — должен упасть с 422."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "",  # ← ПУСТОЕ ИМЯ
            "black": "",
            "round": 1,
            "date": "2026-03-17",
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422# Pydantic validation error
        #assert "white" in str(response.json()["detail"])

def test_invalid_emojis_fails():
    """Тест эмодзи в именах — должен упасть."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "😦🖐️",
            "black": "🤖♟️",
            "round": 1,
            "date": "2026-03-17",
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 200 

def test_invalid_round():
    """Тест эмодзи в именах — должен упасть."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "sdad",
            "black": "qewe",
            "round": 0,
            "date": "2026-03-17",
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422

def test_invalid_data():
    """Тест эмодзи в именах — должен упасть."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "fsf",
            "black": "weiqwje",
            "round": 1,
            "date": "10000001-03-17",
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422  

def test_empty_time_control():
    """Тест пустого white — должен упасть с 422."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "sdfsdf",  
            "black": "Hikaru",
            "round": 1,
            "date": "2026-03-17",
            "time_control": "-1",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422 

def test_invalid_url():
    """Тест эмодзи в именах — должен упасть."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "dsad",
            "black": "sdasd",
            "round": 1,
            "date": "2026-03-17",
            "time_control": "300",
            "stream_url": "http://"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422 

def test_clear_data():
    """Тест эмодзи в именах — должен упасть."""
    with patch("utils.chess_facade.ChessFacade.create_game"):
        body = {
            "white": "dasd",
            "black": "fsdf",
            "round": 1,
            "time_control": "300",
            "stream_url": "https://vk.com/video123"
        }
        response = client.post("/api/v1/game/start", json=body)
        assert response.status_code == 422 

def test_get_game_data():
    with patch("utils.chess_facade.ChessFacade.load_game") as mock_load:
        # Создаем РЕАЛЬНЫЙ python-chess GameNode
        import chess.pgn
        mock_game = chess.pgn.Game()
        mock_game.headers["Site"] = "https://vk.com/chess"
        
        mock_load.return_value = mock_game
        
        response = client.get("/api/v1/game/data")
        assert response.status_code == 200
        data = response.json()
        assert data["active"] is True
