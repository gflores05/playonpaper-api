from fastapi import APIRouter, HTTPException, Depends

from schemas.match import CreateMatch, UpdateMatch, Match
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


@router.get("/", response_model=list[Match])
async def get_all(service: MatchService = Depends(get_match_service)):
    return service.get_all()


@router.get("/{id}", response_model=Match)
async def get_by_id(id: int, service: MatchService = Depends(get_match_service)):
    try:
        return service.get_by_id(id)
    except MatchNotFoundException as error:
        raise HTTPException(status_code=404, detail=error.message)


@router.post("/", response_model=Match)
def create(match: CreateMatch, service: MatchService = Depends(get_match_service)):
    try:
        return service.create(match)
    except CreateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)


@router.patch("/{id}", response_model=Match)
def update(
    id: int, match: UpdateMatch, service: MatchService = Depends(get_match_service)
):
    try:
        return service.update(id, match)
    except UpdateMatchException as error:
        raise HTTPException(status_code=400, detail=error.message)
