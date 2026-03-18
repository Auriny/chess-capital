from fastapi import APIRouter

from routers.v1 import v1_router as v1_router

api_router = APIRouter()

api_router.include_router(v1_router)

_all__ = ("api_router",)
