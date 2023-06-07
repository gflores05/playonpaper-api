from sqlalchemy.orm import Session

from models import Match
from schemas.match import CreateMatch, UpdateMatch


def get(db: Session, id: int):
    return db.query(Match).filter(Match.id == id).first()


def get_all(db: Session):
    return db.query(Match).all()


def create(db: Session, match: CreateMatch):
    db_match = Match(**match.dict())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return db_match


def update(db: Session, id: int, match: UpdateMatch):
    db.query(Match).filter(Match.id == id).update(match.dict())
    db.commit()

    db_match = get(db, id)

    return db_match


def delete(db: Session, id: int):
    db.query(Match).filter(Match.id == id).delete()
    db.commit()
