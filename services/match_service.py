import secrets

from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import (
    match as match_repository,
    game as game_repository,
)
from schemas.match import (
    CreateMatchRequest,
    CreateMatchResponse,
    MatchUpdateEvent,
    UpdateMatchResponse,
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

    def create(self, match: CreateMatchRequest):
        game = game_repository.get(self.db, match.game_id)

        if game is None:
            raise CreateMatchException(f"Game with id {match.game_id} not found")

        code_exists = True

        while code_exists:
            code = secrets.token_urlsafe(8)
            existing_match = match_repository.find(self.db, code=code)

            code_exists = len(existing_match) > 0

        pmp = secrets.token_hex(16)

        challenger = {**match.challenger.dict(), "pmp": pmp}

        new_match = {
            "game_id": match.game_id,
            "code": code,
            "state": match.state,
            "players": {match.challenger.name: challenger},
        }

        match_repository.create(self.db, new_match)

        return CreateMatchResponse(code=code, pmp=pmp)

    def update(self, code: str, match: UpdateMatchRequest):
        db_match = match_repository.find(self.db, code=code)

        if len(db_match) == 0:
            raise UpdateMatchException(f"Match with code {code} doesn't exist")

        db_match = db_match[0]

        if match.winner_id is not None and match.winner_id not in [
            player_id for player_id in db_match.players
        ]:
            raise UpdateMatchException(
                f"The player {match.winner_id} is not in the match"
            )

        player = match.player.dict()

        if match.event == MatchUpdateEvent.PLAYER_JOIN:
            if match.player.name in db_match.players.keys():
                raise UpdateMatchException(
                    f"The player {match.player.name} is already in the game"
                )
            else:
                player = {**player, "pmp": secrets.token_hex(16)}

        else:
            if (
                match.player.name not in db_match.players.keys()
                or db_match.players[match.player.name]["pmp"] != match.player.pmp
            ):
                raise UpdateMatchException(
                    f"You are not allowed to update this player state"
                )
            else:
                player = {**db_match.players[match.player.name], **player}

        updates = {
            "state": {**db_match.state, **match.state},
            "players": {**db_match.players, match.player.name: player},
            "winner_id": match.winner_id,
        }

        updated = match_repository.update(self.db, db_match.id, updates)

        return UpdateMatchResponse(
            code=updated.code,
            state=updated.state,
            pmp=player["pmp"] if match.event == MatchUpdateEvent.PLAYER_JOIN else "",
        )


def get_match_service(db: Session = Depends(get_db)):
    yield MatchService(db)
