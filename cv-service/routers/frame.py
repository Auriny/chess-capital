import json
import asyncio
import aiohttp
import numpy as np
import cv2
import requests

import config as cfg

from typing import Any
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette import status

from recognizer import recognize
from utils import decode_frame
from pprint import pprint

router = APIRouter()
__all__ = ["router"]


@router.post("/frame", tags=["frame"])
async def frame(request: Request):
    body_raw = await request.body()

    if body_raw is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Body cannot be empty"})

    json_body = json.loads(body_raw)

    if "metadata" not in json_body or "frame" not in json_body:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Metadata or frame is empty"})

    board = process_board(json_body)

    return JSONResponse(status_code=status.HTTP_200_OK, content={})


def process_board(json_body: dict[str, Any]):
    frame_type, frame_bytes = decode_frame(json_body["frame"])

    with open("image.png", "wb") as f:
        f.write(frame_bytes)

    decoded = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), -1)
    board = recognize(decoded, json_body["metadata"])

    pprint(board)
    resp = requests.post(
        f"http://{cfg.HOST_NAME}/send",
        headers={"Content-Type": "application/json"},
        data=json.dumps(board)
    )
    print(resp.json())
    return board
