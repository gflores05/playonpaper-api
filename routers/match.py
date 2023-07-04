from fastapi import APIRouter, HTTPException, Depends, Request
from connections.websockets import BroadcastConnectionManager, get_game_ws_manager

from schemas.match import (
    CreateMatchRequest,
    CreateMatchResponse,
    MatchUpdateEvent,
    UpdateMatchResponse,
    UpdateMatchRequest,
    MatchResponse,
)
from services.match_service import (
    CreateMatchException,
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


@router.post("/", response_model=CreateMatchResponse)
def create(
    match: CreateMatchRequest, service: MatchService = Depends(get_match_service)
):
    try:
        return service.create(match)
    except CreateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.patch("/{code}", response_model=UpdateMatchResponse)
async def update(
    code: str,
    match: UpdateMatchRequest,
    service: MatchService = Depends(get_match_service),
    match_ws_manager: BroadcastConnectionManager = Depends(get_game_ws_manager),
):
    try:
        updated = service.update(code, match)

        if match.event == MatchUpdateEvent.STATE_UPDATE:
            await match_ws_manager.broadcast(
                updated.code,
                match.player,
                {"event": MatchUpdateEvent.STATE_UPDATE, "data": updated},
            )

        return updated
    except UpdateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)
