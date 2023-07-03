from sqlalchemy.orm import Session

from models import Match


def get(db: Session, id: int):
    return db.query(Match).filter(Match.id == id).first()


def find(db: Session, **filter):
    return db.query(Match).filter_by(**filter).all()


def get_all(db: Session):
    return db.query(Match).all()


def create(db: Session, match: dict):
    db_match = Match(**match)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return db_match


def update(db: Session, id: int, match: dict):
    db.query(Match).filter(Match.id == id).update(match)
    db.commit()

    db_match = get(db, id)

    return db_match


def delete(db: Session, id: int):
    db.query(Match).filter(Match.id == id).delete()
    db.commit()
