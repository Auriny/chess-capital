from fastapi import APIRouter

from routers.v1.frame import router as frame_router

router = APIRouter(prefix="/v1/cv", tags=["v1"])

router.include_router(frame_router)

__all__ = ["router"]