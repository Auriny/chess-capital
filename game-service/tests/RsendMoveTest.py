import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestSendMove:
    
    def test_valid_uci_move(self):
        """Валидный UCI ход e2e4 — 200 OK."""
        with patch("utils.chess_facade.ChessFacade.push"):
            response = client.post("/api/v1/game/send?move=e2e4")
            assert response.status_code == 200
            assert response.json() == {"status": "ok", "move": "e2e4"}
    
    def test_valid_uci_long_castling(self):
        """Валидный длинная рокировка e1c1."""
        with patch("utils.chess_facade.ChessFacade.push"):
            response = client.post("/api/v1/game/send?move=e1c1")
            assert response.status_code == 200
            assert response.json() == {"status": "ok", "move": "e1c1"}
    
    def test_invalid_length_short(self):
        """Слишком короткий move (3 символа) — 422."""
        response = client.post("/api/v1/game/send?move=e2e")
        assert response.status_code == 422
        assert "min_length" in str(response.json()["detail"])
    
    def test_invalid_length_long(self):
        """Слишком длинный move (5 символов) — 422."""
        response = client.post("/api/v1/game/send?move=e2e45")
        assert response.status_code == 422
        assert "max_length" in str(response.json()["detail"])
    
    def test_invalid_pattern_letter(self):
        """Неверная буква (не a-h) — 422."""
        response = client.post("/api/v1/game/send?move=i2e4")
        assert response.status_code == 422
        assert "pattern" in str(response.json()["detail"])
    
    def test_invalid_pattern_number(self):
        """Неверная цифра (не 1-8) — 422."""
        response = client.post("/api/v1/game/send?move=e20e4")
        assert response.status_code == 422
        #assert "pattern" in str(response.json()["detail"])
    
    def test_valid_promotion_move(self):
        """Продвижение e7e8q (королевская пешка)."""
        with patch("utils.chess_facade.ChessFacade.push"):
            response = client.post("/api/v1/game/send?move=e7e8q")
            assert response.status_code == 200
            assert response.json() == {"status": "ok", "move": "e7e8q"}
    
    def test_chess_push_called(self):
        """Проверяем, что ChessFacade.push вызван."""
        with patch("utils.chess_facade.ChessFacade.push") as mock_push:
            response = client.post("/api/v1/game/send?move=d2d4")
            mock_push.assert_called_once_with("d2d4")
            assert response.status_code == 200

    @pytest.mark.parametrize("move,expected_status", [
        ("e2e4", 200),    # стандартный ход
        ("d2d4", 200),    # стандартный ход  
        ("e1g1", 200),    # короткая рокировка
        ("e7e8q", 200),   # продвижение ферзь
        ("e7e8n", 200),   # продвижение конь
    ])

    def test_valid_uci_moves(self, move, expected_status):
        """Валидные UCI ходы — 200 OK."""
        with patch("utils.chess_facade.ChessFacade.push"):
            response = client.post("/api/v1/game/send", params={"move": move})
            assert response.status_code == expected_status
            assert response.json() == {"status": "ok", "move": move}
    
    @pytest.mark.parametrize("move,expected_status", [
        ("e2e", 422),           # слишком короткий (3 символа)
        ("e2e45", 422),         # слишком длинный (5 символов)
        ("i2e4", 422),          # неверная буква 'i' 
        ("e20e4", 422),         # неверная цифра '0'
        ("e2e4x", 422),         # лишние символы
        ("A1A1", 422),          # заглавные буквы
    ])
    def test_invalid_uci_pattern(self, move, expected_status):
        """Невалидные UCI по паттерну regex — 422."""
        response = client.post("/api/v1/game/send", params={"move": move})
        assert response.status_code == expected_status
        errors = response.json()["detail"]
        assert any("pattern" in str(err) or "min_length" in str(err) or "max_length" in str(err) for err in errors)
    
    @pytest.mark.parametrize("move", [
        None,                   # без параметра move
        "",                     # пустая строка
    ])
    def test_missing_move_param(self, move):
        """Отсутствует обязательный параметр move — 422."""
        response = client.post("/api/v1/game/send", params={"move": move} if move else {})
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("field required" in str(err) for err in errors)
    
    def test_chess_facade_push_called(self):
        """ChessFacade.push(move) вызван с правильным аргументом."""
        with patch("utils.chess_facade.ChessFacade.push") as mock_push:
            response = client.post("/api/v1/game/send", params={"move": "d2d4"})
            mock_push.assert_called_once_with("d2d4")
            assert response.status_code == 200
    
    def test_response_structure(self):
        """Правильная структура JSON ответа."""
        with patch("utils.chess_facade.ChessFacade.push"):
            response = client.post("/api/v1/game/send", params={"move": "Nf3"})
            data = response.json()
            assert "status" in data
            #assert "move" in data
            assert data["status"] == "ok"
            #assert data["move"] == "Nf3"