"""In-memory store for jogos, exposed as pure-ish functions.

The state is a single module-level dict. All operations are functions that
either read from or return new state, keeping route handlers free of
class-based logic.
"""
from typing import Dict, List, Optional
from uuid import uuid4

from models import Jogo


_jogos: Dict[str, Jogo] = {}


def list_jogos() -> List[Jogo]:
    return list(_jogos.values())


def get_jogo(jogo_id: str) -> Optional[Jogo]:
    return _jogos.get(jogo_id)


def create_jogo(time_a: str, pontos_a: int, time_b: str, pontos_b: int) -> Jogo:
    if time_a == time_b:
        raise ValueError("Os dois times devem ser diferentes")
    if pontos_a < 0 or pontos_b < 0:
        raise ValueError("Pontos não podem ser negativos")

    jogo = Jogo(
        id=str(uuid4()),
        times={time_a: pontos_a, time_b: pontos_b},
    )
    _jogos[jogo.id] = jogo
    return jogo


def reset() -> None:
    _jogos.clear()
