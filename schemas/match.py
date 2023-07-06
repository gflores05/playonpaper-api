from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel

from .player import Player
from .game import GameResponse


class MatchPlayerResponse(BaseModel):
    state: dict
    name: str


class MatchResponse(BaseModel):
    id: int
    start_date: datetime
    end_date: Optional[datetime]
    state: Optional[dict]
    status: str
    players: Dict[str, MatchPlayerResponse]
    code: str
    winner: Optional[Player]
    game: GameResponse

    class Config:
        orm_mode = True


class MatchPlayerRequest(BaseModel):
    name: str
    pmp: Optional[str]
    state: dict


class CreateMatchRequest(BaseModel):
    state: dict
    game_id: int


class MatchUpdateEvent(Enum):
    STATE_UPDATE = 1
    PLAYER_LEFT = 2
    PLAYER_JOIN = 3


class MatchStatus(Enum):
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    ENDED = "ENDED"


class UpdateMatchRequest(BaseModel):
    winner_id: Optional[int]
    status: Optional[MatchStatus]
    player: MatchPlayerRequest
    state: dict


class JoinMatchRequest(BaseModel):
    player: MatchPlayerRequest


class JoinMatchResponse(BaseModel):
    pmp: str
