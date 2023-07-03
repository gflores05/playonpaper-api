from sqlalchemy.orm import Session

from models import Game
from schemas.game import CreateGameRequest, UpdateGameRequest


def get(db: Session, id: int):
    return db.query(Game).filter(Game.id == id).first()


def find(db: Session, **filter):
    return db.query(Game).filter_by(**filter).all()


def get_all(db: Session):
    return db.query(Game).all()


def create(db: Session, game: CreateGameRequest):
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def update(db: Session, id: int, game: UpdateGameRequest):
    db.query(Game).filter(Game.id == id).update(game.dict())
    db.commit()

    db_game = get(db, id)

    return db_game
