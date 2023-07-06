import json
from fastapi import APIRouter, HTTPException, Depends, Request
from connections.websockets import BroadcastConnectionManager, get_game_ws_manager

from schemas.match import (
    CreateMatchRequest,
    JoinMatchRequest,
    JoinMatchResponse,
    MatchUpdateEvent,
    UpdateMatchRequest,
    MatchResponse,
)
from services.match_service import (
    CreateMatchException,
    JoinMatchException,
    MatchNotFoundException,
    MatchService,
    UpdateMatchException,
    get_match_service,
)

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[MatchResponse])
async def get_all(req: Request, service: MatchService = Depends(get_match_service)):
    if len(req.query_params.keys()) == 0:
        return service.get_all()
    else:
        return service.find(**req.query_params)


@router.get("/{id}", response_model=MatchResponse)
async def get_by_id(id: int, service: MatchService = Depends(get_match_service)):
    try:
        return service.get_by_id(id)
    except MatchNotFoundException as error:
        raise HTTPException(status_code=404, detail=error.message)


@router.post("/", response_model=MatchResponse)
def create(
    payload: CreateMatchRequest, service: MatchService = Depends(get_match_service)
):
    try:
        return service.create(payload)
    except CreateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.patch("/{id}", response_model=MatchResponse)
async def update(
    id: int,
    payload: UpdateMatchRequest,
    service: MatchService = Depends(get_match_service),
    match_ws_manager: BroadcastConnectionManager = Depends(get_game_ws_manager),
):
    try:
        updated = service.update(id, payload)

        await match_ws_manager.broadcast(
            updated.code,
            payload.player.name,
            {
                "event": MatchUpdateEvent.STATE_UPDATE.value,
                "data": json.loads(MatchResponse.from_orm(updated).json()),
            },
        )

        return updated
    except UpdateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.post("/{code}/join", response_model=JoinMatchResponse)
async def join(
    code: str,
    payload: JoinMatchRequest,
    service: MatchService = Depends(get_match_service),
    match_ws_manager: BroadcastConnectionManager = Depends(get_game_ws_manager),
):
    try:
        updated = service.join(code, payload)

        await match_ws_manager.broadcast(
            code,
            payload.player.name,
            {"event": MatchUpdateEvent.PLAYER_JOIN.value, "data": payload.player.name},
        )

        return updated
    except JoinMatchException as error:
        raise HTTPException(status_code=403, detail=error.message)
