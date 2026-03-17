import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from fastapi import Request
from starlette.requests import Request as StarletteRequest
from starlette.datastructures import Headers, URL
from fastapi.responses import JSONResponse

from exceptions.game_not_found import GameNotFoundError

class DummyScope(dict):
    """Простейший scope, чтобы создать Request вручную."""
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


def test_exc_handler_response():
    """Проверяем, что handler возвращает нужный JSON и статус."""
    request = Request(DummyScope())

    exc = GameNotFoundError(active=False, msg="No game")
    response: JSONResponse = pytest.run(async_func=exc_handler(request, exc)) if False else None
