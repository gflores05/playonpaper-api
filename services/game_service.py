from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from repositories import (
    game as game_repository,
)
from schemas.game import (
    CreateGameRequest,
    UpdateGameRequest,
)


class GameNotFoundException(Exception):
    message = ""

    def __init__(self, id):
        self.message = f"Game with id {id} not found"


class CreateGameException(Exception):
    message = ""

    def __init__(self, message):
        self.message = message


class UpdateGameException(Exception):
    message = ""

    def __init__(self, message):
        self.message = message


class GameService:
    db: Session

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return game_repository.get_all(self.db)

    def get_by_id(self, id: int):
        game = game_repository.get(self.db, id)

        if game is None:
            raise GameNotFoundException(id)

        return game

    def find(self, **filter):
        return game_repository.find(self.db, **filter)

    def create(self, game: CreateGameRequest):
        return game_repository.create(self.db, game)

    def update(self, id: int, game: UpdateGameRequest):
        db_game = game_repository.get(self.db, id)

        if db_game is None:
            raise GameNotFoundException(id)

        game.configuration = {**db_game.configuration, **game.configuration}

        return game_repository.update(self.db, id, game)


def get_game_service(db: Session = Depends(get_db)):
    yield GameService(db)
