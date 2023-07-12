import secrets
from datetime import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import (
    match as match_repository,
    game as game_repository,
)
from schemas.match import (
    CreateMatchRequest,
    JoinMatchRequest,
    JoinMatchResponse,
    MatchStatus,
    UpdateMatchRequest,
)


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


class JoinMatchException(Exception):
    message = ""

    def __init__(self, code):
        self.message = f"You are not allowed to join match with code: {code}"


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

    def find(self, **filter):
        return match_repository.find(self.db, **filter)

    def generate_code(self):
        code_exists = True
        code = ""
        while code_exists:
            code = secrets.token_urlsafe(8)
            existing_match = match_repository.find(self.db, code=code)

            code_exists = len(existing_match) > 0

        return code

    def create(self, payload: CreateMatchRequest):
        game = game_repository.get(self.db, payload.game_id)

        if game is None:
            raise CreateMatchException(f"Game with id {payload.game_id} not found")

        code = self.generate_code()

        new_match = {
            "game_id": payload.game_id,
            "code": code,
            "state": payload.state,
            "status": MatchStatus.WAITING.value,
            "players": {},
        }

        return match_repository.create(self.db, new_match)

    def get_by_code(self, code: str):
        db_match = match_repository.find(self.db, code=code)

        if len(db_match) == 0:
            raise UpdateMatchException(f"Match with code {code} doesn't exist")

        return db_match[0]

    def join(self, code: str, payload: JoinMatchRequest):
        db_match = self.get_by_code(code)

        if payload.player.name not in db_match.players.keys():
            player = {**payload.player.dict(), "pmp": secrets.token_hex(16)}

            match_repository.update(
                self.db,
                db_match.id,
                {"players": {**db_match.players, payload.player.name: player}},
            )

            return JoinMatchResponse(pmp=player["pmp"])
        elif db_match.players[payload.player.name] != payload.player.pmp:
            raise JoinMatchException(code)

        return JoinMatchResponse(pmp=payload.player.pmp)

    def update(self, id: int, payload: UpdateMatchRequest):
        db_match = self.get_by_id(id)

        if payload.winner_id is not None and payload.winner_id not in [
            player_id for player_id in db_match.players
        ]:
            raise UpdateMatchException(
                f"The player {payload.winner_id} is not in the match"
            )

        player = payload.player.dict()

        if (
            payload.player.name not in db_match.players.keys()
            or db_match.players[payload.player.name]["pmp"] != payload.player.pmp
        ):
            raise UpdateMatchException(f"You are not allowed to update this match")
        else:
            player = {**db_match.players[payload.player.name], **player}

        updates = {
            "state": {**db_match.state, **payload.state},
            "players": {**db_match.players, payload.player.name: player},
            "winner_id": payload.winner_id,
            "status": MatchStatus.PLAYING.value
            if payload.status is None
            else payload.status.value,
        }

        if payload.status == "ENDED":
            updates["end_date"] = datetime.now()

        return match_repository.update(self.db, db_match.id, updates)


def get_match_service(db: Session = Depends(get_db)):
    yield MatchService(db)
