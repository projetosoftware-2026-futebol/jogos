from enum import Enum
from typing import Dict
from pydantic import BaseModel, Field


class Status(str, Enum):
    SCHEDULED = "scheduled"
    PLAYING = "playing"
    FINISHED = "finished"


class Jogo(BaseModel):
    id: str
    times: Dict[str, int] = Field(default_factory=dict)
    status: Status = Status.SCHEDULED


class PlayRequest(BaseModel):
    time_a: str
    time_b: str


class ScoreRequest(BaseModel):
    time: str
    pontos: int = 1


class FinishRequest(BaseModel):
    pass
