from fastapi import APIRouter, HTTPException, Depends, Request

from schemas.game import CreateGameRequest, UpdateGameRequest, GameResponse
from services.game_service import GameNotFoundException, GameService, get_game_service

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[GameResponse])
async def get_all(req: Request, service: GameService = Depends(get_game_service)):
    if len(req.query_params.keys()) == 0:
        return service.get_all()
    else:
        return service.find(**req.query_params)


@router.get("/{id}", response_model=GameResponse)
async def get_by_id(id: int, service: GameService = Depends(get_game_service)):
    try:
        return service.get_by_id(id)
    except GameNotFoundException as error:
        raise HTTPException(status_code=404, detail=error.message)


@router.post("/", response_model=GameResponse)
def create(game: CreateGameRequest, service: GameService = Depends(get_game_service)):
    return service.create(game)


@router.patch("/{id}", response_model=GameResponse)
def update(
    id: int, game: UpdateGameRequest, service: GameService = Depends(get_game_service)
):
    try:
        return service.update(id, game)
    except GameNotFoundException as error:
        raise HTTPException(status_code=404, detail=error.message)
