from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import game as game_repository, player as player_repository
from schemas.game import CreateGame, UpdateGame, Game

router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Game])
async def get_all(db: Session = Depends(get_db)):
    return game_repository.get_all(db)


@router.get("/{id}", response_model=Game)
async def get_by_id(id: int, db: Session = Depends(get_db)):
    game = game_repository.get(db, id)

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


@router.post("/", response_model=Game)
def create(game: CreateGame, db: Session = Depends(get_db)):
    return game_repository.create(db, game)


@router.patch("/{id}", response_model=Game)
def update(id: int, game: UpdateGame, db: Session = Depends(get_db)):
    db_game = game_repository.get(db, id)

    if db_game is None:
        raise HTTPException(status_code=400, detail=f"Game with {id} doesn't exist")

    return game_repository.update(db, id, game)
