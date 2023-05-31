from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from player import Player
from game import Game


class Match(BaseModel):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    state: Optional[dict]
    players: list[Player]
    winner: Optional[Player]
    game: Game

    class Config:
        orm_mode = True


class CreateMatch(BaseModel):
    state: dict
    game_id: int
    players: list[int]


class UpdateGame(BaseModel):
    winner_id: Optional[int]
    state: dict
