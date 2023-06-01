from sqlalchemy.orm import Session

from models import Game
from schemas.game import CreateGame, UpdateGame


def get(db: Session, id: int):
    return db.query(Game).filter(Game.id == id).first()


def get_all(db: Session):
    return db.query(Game).all()


def create(db: Session, game: CreateGame):
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    return db_game


def update(db: Session, id: int, game: UpdateGame):
    db.query(Game).filter(Game.id == id).update(game.dict())
    db.commit()

    db_game = get(db, id)

    return db_game
