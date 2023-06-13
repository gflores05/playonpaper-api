from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connections.websockets import UnicastConnectionManager, BroadcastConnectionManager

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

broadcast_manager = BroadcastConnectionManager()
unicast_manager = UnicastConnectionManager()


@router.websocket("/{sender_id}")
async def send_message(websocket: WebSocket, sender_id: str):
    await unicast_manager.connect(sender_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await unicast_manager.send_message(
                sender_id, data["recipient"], data["content"]
            )
    except WebSocketDisconnect:
        unicast_manager.disconnect(sender_id)


@router.websocket("/{room}/{sender_id}")
async def broadcast(websocket: WebSocket, room: str, sender_id: str):
    await broadcast_manager.connect(room, sender_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await broadcast_manager.broadcast(room, sender_id, data["content"])
    except WebSocketDisconnect:
        broadcast_manager.disconnect(room, sender_id)
        await broadcast_manager.broadcast(
            room, sender_id, f"{sender_id} has left the chat"
        )
