from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .player import Player
from .game import Game


class Match(BaseModel):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    state: Optional[dict]
    players: dict
    code: str
    winner: Optional[Player]
    game: Game

    class Config:
        orm_mode = True


class PlayerMatch(BaseModel):
    name: str
    state: dict


class CreateMatch(BaseModel):
    state: dict
    game_id: int
    challenger: PlayerMatch


class UpdateMatch(BaseModel):
    winner_id: Optional[int]
    players: Optional[dict]
    state: dict
