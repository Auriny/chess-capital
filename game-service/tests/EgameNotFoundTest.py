import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from exceptions import GameNotFoundError


def test_game_not_found_error_attributes():
    """Проверяем, что атрибуты active и message задаются корректно."""
    exc = GameNotFoundError(active=False, msg="Game not found")

    assert isinstance(exc, GameNotFoundError)
    assert exc.active is False
    assert exc.message == "Game not found"


def test_game_not_found_error_raised():
    """Проверяем, что исключение можно выбросить и поймать через pytest.raises."""
    with pytest.raises(GameNotFoundError) as exc_info:
        raise GameNotFoundError(active=True, msg="No active game")

    exc = exc_info.value  # сам объект исключения [web:170][web:171]
    assert exc.active is True
    assert exc.message == "No active game"
