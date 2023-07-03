from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from connections.websockets import BroadcastConnectionManager, get_game_ws_manager
from schemas.match import MatchUpdateEvent

router = APIRouter(
    prefix="/match",
    tags=["match"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/{match_code}/{player}")
async def update_game_state(
    websocket: WebSocket,
    match_code: str,
    player: str,
    match_ws_manager: BroadcastConnectionManager = Depends(get_game_ws_manager),
):
    await match_ws_manager.connect(match_code, player, websocket)

    try:
        await match_ws_manager.broadcast(
            match_code,
            player,
            {"type": MatchUpdateEvent.PLAYER_JOIN.name, "player": player},
        )
    except WebSocketDisconnect:
        match_ws_manager.disconnect(match_code, player)
        await match_ws_manager.broadcast(
            match_code,
            player,
            {"type": MatchUpdateEvent.PLAYER_LEFT.name, "player": player},
        )
