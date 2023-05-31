from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

Base = declarative_base()


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    configuration = Column(JSONB, default={"enabled": False})
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    points = Column(Integer, default=0, nullable=False)
    date_created = Column(DateTime, nullable=False, server_default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())


class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    players = Column(ARRAY(JSONB), nullable=False)
    state = Column(JSONB)
    start_date = Column(DateTime, server_default=func.now(), nullable=False)
    end_date = Column(DateTime, onupdate=func.now())
    winner_id = Column(Integer, ForeignKey("player.id"))

    winner = relationship("Player", foreign_keys=[winner_id])
    game = relationship("Game", foreign_keys=[game_id])
