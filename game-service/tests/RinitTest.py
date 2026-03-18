import pytest, os, sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from unittest.mock import patch
from fastapi import APIRouter
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_v1_router_instance():
    """Проверяем, что v1_router создан."""
    from routers.v1 import v1_router
    assert isinstance(v1_router, APIRouter)

def test_v1_router_prefix():
    """Проверяем prefix='/v1/game' и tags."""
    from routers.v1 import v1_router
    assert v1_router.prefix == "/v1/game"
    assert v1_router.tags == ["V1"]

def test_subrouters_included():
    """Проверяем include_router ДО переноса routes."""
    from routers.v1 import v1_router
    from routers.v1.game_process import router as game_process
    from routers.v1.send_move import router as send_move
    
    # СНАЧАЛА сохраняем оригинальные роуты
    game_original_routes = len(game_process.routes)
    send_original_routes = len(send_move.routes)
    
    # include_router НЕ копирует routes, а ПЕРЕНOSIТ
    assert len(v1_router.routes) > 0  # Роуты теперь в v1_router
    #assert len(game_process.routes) == 0  # game_process опустел!
    #assert len(send_move.routes) == 0    # send_move опустел!
    
    # Проверяем, что роуты перенесены
    v1_paths = {r.path for r in v1_router.routes if hasattr(r, 'path')}
    assert "/v1/game/start" in v1_paths
    assert "/v1/game/data" in v1_paths
    assert "/v1/game/send" in v1_paths


def test_v1_router_in_api():
    """Проверяем, что v1_router включен в app через api_router."""
    from routers import api_router
    from routers.v1 import v1_router
    
    # Полные пути в app: /api + /v1/game + /start
    app_paths = {r.path for r in app.routes}
    assert "/api/v1/game/start" in app_paths
    assert "/api/v1/game/data" in app_paths
    assert "/api/v1/game/send" in app_paths

def test_full_endpoints_accessible():
    """Интеграционный тест — все эндпоинты v1 доступны."""
    response = client.get("/api/v1/game/data")
    assert response.status_code in [200, 422]  # 200 или валидация
    
    response = client.post("/api/v1/game/send?move=e2e4")
    assert response.status_code in [200, 422]
    
    response = client.post("/api/v1/game/start", json={})
    assert response.status_code in [200, 422]
