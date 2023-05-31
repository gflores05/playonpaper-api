from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    level: int
    points: int
    date_created: datetime
    date_updated: Optional[datetime]

    class Config:
        orm_mode = True


class CreatePlayer(BaseModel):
    name: str


class UpdatePlayer(BaseModel):
    level: int
    points: int
