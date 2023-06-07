from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import (
    match as match_repository,
    player as player_repository,
    game as game_repository,
)
from schemas.match import CreateMatch, UpdateMatch, Match

router = APIRouter(
    prefix="/matches",
    tags=["matches"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Match])
async def get_all(db: Session = Depends(get_db)):
    return match_repository.get_all(db)


@router.get("/{id}", response_model=Match)
async def get_by_id(id: int, db: Session = Depends(get_db)):
    match = match_repository.get(db, id)

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    return match


@router.post("/", response_model=Match)
def create(match: CreateMatch, db: Session = Depends(get_db)):
    game = game_repository.get(db, match.game_id)

    if game is None:
        raise HTTPException(
            status_code=400, detail=f"Game with id {match.game_id} not found"
        )

    player_ids = list(dict.fromkeys(match.players))

    if len(player_ids) != len(match.players):
        raise HTTPException(
            status_code=400, detail="A player cannot be added more than once"
        )

    players = player_repository.get_many(db, match.players)

    if len(players) != len(player_ids):
        found_player_ids = [player.id for player in players]

        not_found_players = [
            player_id for player_id in player_ids if player_id not in found_player_ids
        ]

        raise HTTPException(
            status_code=400, detail=f"Invalid player(s) {not_found_players}"
        )

    return match_repository.create(db, match)


@router.patch("/{id}", response_model=Match)
def update(id: int, match: UpdateMatch, db: Session = Depends(get_db)):
    db_match = match_repository.get(db, id)

    if db_match is None:
        raise HTTPException(status_code=404, detail=f"Match with {id} doesn't exist")

    if match.winner_id not in [player_id for player_id in db_match.players]:
        raise HTTPException(
            status_code=400, detail=f"The player {match.winner_id} is not in the match"
        )

    return match_repository.update(db, id, match)
