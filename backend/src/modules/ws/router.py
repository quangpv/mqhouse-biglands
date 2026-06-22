import logging

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from src.platform.security import decode_jwt
from src.platform.ws_manager import ConnectionManager, get_ws_manager

logger = logging.getLogger("biglands.ws")

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    ws: WebSocket,
    token: str = Query(...),
    ws_manager: ConnectionManager = Depends(get_ws_manager),
):
    payload = decode_jwt(token)
    user_id = payload.get("sub")
    if user_id is None:
        logger.warning("WebSocket auth failed: invalid token")
        await ws.close(code=4001)
        return
    logger.info("WebSocket connected: user_id=%s", user_id)
    await ws_manager.connect(user_id, ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, ws)
