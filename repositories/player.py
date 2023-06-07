from sqlalchemy.orm import Session

from models import Player
from schemas.player import CreatePlayer, UpdatePlayer


def get(db: Session, id: int):
    return db.query(Player).filter(Player.id == id).first()


def get_by_name(db: Session, name: str):
    return db.query(Player).filter(Player.name == name).first()


def get_many(db: Session, player_ids: list[int]):
    return db.query(Player).filter(Player.id.in_(player_ids)).all()


def get_all(db: Session):
    return db.query(Player).all()


def create(db: Session, player: CreatePlayer):
    db_player = Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player


def update(db: Session, id: int, player: UpdatePlayer):
    db.query(Player).filter(Player.id == id).update(player.dict())
    db.commit()

    db_player = get(db, id)

    return db_player


def delete(db: Session, id: int):
    db.query(Player).filter(Player.id == id).delete()
    db.commit()
