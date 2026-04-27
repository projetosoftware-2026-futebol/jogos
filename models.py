from typing import Dict
from pydantic import BaseModel, Field


class Jogo(BaseModel):
    id: str
    times: Dict[str, int] = Field(default_factory=dict)


class PlayRequest(BaseModel):
    time_a: str
    pontos_a: int = 0
    time_b: str
    pontos_b: int = 0
