from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from connections.websockets import (
    UnicastConnectionManager,
    BroadcastConnectionManager,
    get_chat_unicast_ws_manager,
    get_chat_broadcast_ws_manager,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/{sender_id}")
async def send_message(
    websocket: WebSocket,
    sender_id: str,
    ws_manager: UnicastConnectionManager = Depends(get_chat_unicast_ws_manager),
):
    await ws_manager.connect(sender_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.send_message(sender_id, data["recipient"], data["content"])
    except WebSocketDisconnect:
        ws_manager.disconnect(sender_id)


@router.websocket("/{room}/{sender_id}")
async def broadcast(
    websocket: WebSocket,
    room: str,
    sender_id: str,
    ws_manager: BroadcastConnectionManager = Depends(get_chat_broadcast_ws_manager),
):
    await ws_manager.connect(room, sender_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await ws_manager.broadcast(room, sender_id, data["content"])
    except WebSocketDisconnect:
        ws_manager.disconnect(room, sender_id)
        await ws_manager.broadcast(room, sender_id, f"{sender_id} has left the chat")
