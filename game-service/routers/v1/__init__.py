from fastapi import APIRouter

from routers.v1.game_process import router as game_process_router
from routers.v1.send_move import router as send_move_router

v1_router = APIRouter(tags=["V1"])

v1_router.include_router(send_move_router)
v1_router.include_router(game_process_router)

__all__ = ("v1_router",)
