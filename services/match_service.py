import secrets

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import (
    match as match_repository,
    game as game_repository,
)
from schemas.match import CreateMatch, UpdateMatch


class MatchNotFoundException(Exception):
    message = ""

    def __init__(self, id):
        self.message = f"Match with id {id} not found"


class CreateMatchException(Exception):
    message = ""

    def __init__(self, message):
        self.message = message


class UpdateMatchException(Exception):
    message = ""

    def __init__(self, message):
        self.message = message


class MatchService:
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return match_repository.get_all(self.db)

    def get_by_id(self, id: int):
        match = match_repository.get(self.db, id)

        if match is None:
            raise MatchNotFoundException(id)

        return match

    def create(self, match: CreateMatch):
        game = game_repository.get(self.db, match.game_id)

        if game is None:
            raise CreateMatchException(f"Game with id {match.game_id} not found")

        code_exists = True

        while code_exists:
            code = secrets.token_urlsafe(8)
            existing_match = match_repository.get_first_by(self.db, code=code)

            code_exists = existing_match is not None

        new_match = {
            "game_id": match.game_id,
            "code": code,
            "state": match.state,
            "players": {match.challenger.name: match.challenger.dict()},
        }

        return match_repository.create(self.db, new_match)

    def update(self, id: int, match: UpdateMatch):
        db_match = match_repository.get(self.db, id)

        if db_match is None:
            raise UpdateMatchException(f"Match with {id} doesn't exist")

        if match.winner_id is not None and match.winner_id not in [
            player_id for player_id in db_match.players
        ]:
            raise UpdateMatchException(
                f"The player {match.winner_id} is not in the match"
            )

        updates = {
            "state": {**db_match.state, **match.state},
            "players": {**db_match.players, **match.players},
            "winner_id": match.winner_id,
        }

        return match_repository.update(self.db, id, updates)


def get_match_service(db: Session = Depends(get_db)):
    yield MatchService(db)
