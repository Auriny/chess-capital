import asyncio
import pytest, os, sys, json

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from fastapi import Request
from starlette.datastructures import Headers, URL
from fastapi.responses import JSONResponse
from chess import IllegalMoveError

from exceptions.game_not_found import GameNotFoundError
from exceptions import game_not_found_handler, illegal_move_handler


class DummyScope(dict):
    """Простой scope чтобы создать Request."""
    def __init__(self):
        super().__init__(
            {
                "type": "http",
                "method": "GET",
                "path": "/",
                "headers": [],
                "query_string": b"",
                "client": ("testclient", 50000),
                "server": ("testserver", 80),
                "scheme": "http",
            }
        )


def _fake_request() -> Request:
    return Request(DummyScope())


def test_game_not_found_handler_response():
    """Проверяем JSON и статус для GameNotFoundError."""
    request = _fake_request()
    exc = GameNotFoundError(active=False, msg="No game")

    response: JSONResponse = asyncio.run(game_not_found_handler(request, exc))

    assert response.status_code == 200
    data = json.loads(response.body)
    assert data == {"active": False, "message": "No game"}


def test_illegal_move_handler_response():
    """Проверяем JSON и статус для IllegalMoveError."""
    request = _fake_request()
    exc = IllegalMoveError("illegal move", 1)

    response: JSONResponse = asyncio.run(illegal_move_handler(request, exc))

    assert response.status_code == 400
    data = json.loads(response.body)
    # exc.args → кортеж, JSON сериализует в список
    assert data == {"details": ["illegal move", 1]}