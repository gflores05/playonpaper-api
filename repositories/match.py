from sqlalchemy.orm import Session

from models import Match
from schemas.match import CreateMatch, UpdateMatch


def get(db: Session, id: int):
    return db.query(Match).filter(Match.id == id).first()


def get_all(db: Session):
    return db.query(Match).all()


def create(db: Session, Match: CreateMatch):
    db_Match = Match(name=Match.name)
    db.add(db_Match)
    db.commit()
    db.refresh(db_Match)

    return db_Match


def update(db: Session, id: int, Match: UpdateMatch):
    db.query(Match).filter(Match.id == id).update(Match.dict())
    db.commit()

    db_Match = get(db, id)

    return db_Match


def delete(db: Session, id: int):
    db.query(Match).filter(Match.id == id).delete()
    db.commit()
