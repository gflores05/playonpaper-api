from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Game(BaseModel):
    id: int
    name: str
    code: str
    configuration: dict
    date_created: datetime
    date_updated: Optional[datetime]

    class Config:
        orm_mode = True


class CreateGame(BaseModel):
    name: str
    code: str
    configuration: dict


class UpdateGame(BaseModel):
    name: str
    configuration: dict
