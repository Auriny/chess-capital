import pytest
import sys
import os
from unittest.mock import MagicMock
from fastapi import FastAPI

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from main import app
from exceptions import exc_handler 
from routers import api_router

def test_app_instance():
    """Проверяем, что main.py создает FastAPI приложение"""
    assert isinstance(app, FastAPI) 

def test_app_title():
    """Проверяем title приложения"""
    assert app.title == "Chess Capital Backend" 

def test_app_exception_handler():
    """Проверяем регистрацию exception handler"""
    assert exc_handler in app.exception_handlers.values() 

def test_api_router_included():
    """Проверяем, что api_router включен в app"""
    app_routes = [r.path for r in app.routes]
    api_routes = [r.path for r in api_router.routes if hasattr(r, 'path')]
    overlap = set(app_routes) & set(api_routes)
    assert len(overlap) > 0 or api_router in [r.include_in_app for r in app.routes if hasattr(r, 'include_in_app')] 
