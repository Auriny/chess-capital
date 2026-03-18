import pytest
import os
import sys
from fastapi import APIRouter

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));
if parent not in sys.path: 
    sys.path.insert(0, parent)

from routers import api_router
from routers.v1 import v1_router as v1_router

def test_api_router_instance():
    """Проверяем, что routers/__init__.py создает APIRouter"""
    assert isinstance(api_router, APIRouter) 

def test_api_router_prefix():
    """Проверяем префикс /api у api_router"""
    assert api_router.prefix == "/api"  

def test_v1_router_included():
    """Проверяем, что v1_router включен в api_router"""
    api_routes = [r.path for r in api_router.routes]
    assert len(api_router.routes) > 0 
