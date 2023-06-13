from fastapi import WebSocket
from typing import Dict


class UnicastConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()

        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)

    async def send_message(self, sender_id: str, recipient_id: str, message: str):
        if recipient_id in self.active_connections.keys():
            await self.active_connections[recipient_id].send_json(
                {"sender": sender_id, "content": message}
            )


class BroadcastConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, room: str, client_id: str, websocket: WebSocket):
        await websocket.accept()

        if room in self.active_connections.keys():
            self.active_connections[room][client_id] = websocket
        else:
            self.active_connections[room] = {client_id: websocket}

    def disconnect(self, room: str, client_id: str):
        if room in self.active_connections.keys():
            self.active_connections[room].pop(client_id, None)

            if len(self.active_connections[room].keys()) == 0:
                self.active_connections.pop(room)

    async def broadcast(self, room: str, sender_id: str, message: str):
        for client_id, connection in self.active_connections[room].items():
            if sender_id != client_id:
                await connection.send_json({"sender": sender_id, "content": message})
