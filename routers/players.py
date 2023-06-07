from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import player as player_repository
from schemas.player import CreatePlayer, UpdatePlayer, Player

router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Player])
def get_all(db: Session = Depends(get_db), name: str = None):
    if name:
        return player_repository.get_by_name(db, name)

    players = player_repository.get_all(db)
    return players


@router.get("/{id}", response_model=Player)
def get_by_id(id: int, db: Session = Depends(get_db)):
    player = player_repository.get(db, id)

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@router.post("/", response_model=Player)
def create(player: CreatePlayer, db: Session = Depends(get_db)):
    if player_repository.get_by_name(db, player.name):
        raise HTTPException(
            status_code=400, detail=f'"{player.name}" has been already taken'
        )

    return player_repository.create(db, player)


@router.patch("/{id}", response_model=Player)
def update(id: int, player: UpdatePlayer, db: Session = Depends(get_db)):
    if player_repository.get(db, id) is None:
        raise HTTPException(status_code=404, detail=f"Player with {id} doesn't exist")

    return player_repository.update(db, id, player)
