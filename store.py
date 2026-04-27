"""In-memory store for jogos, exposed as pure-ish functions.

The state is a single module-level dict. All operations are functions that
either read from or return new state, keeping route handlers free of
class-based logic.
"""
from typing import Dict, List, Optional
from uuid import uuid4

from models import Jogo, Status


_jogos: Dict[str, Jogo] = {}


def list_jogos() -> List[Jogo]:
    return list(_jogos.values())


def get_jogo(jogo_id: str) -> Optional[Jogo]:
    return _jogos.get(jogo_id)


def create_jogo(time_a: str, time_b: str) -> Jogo:
    if time_a == time_b:
        raise ValueError("Os dois times devem ser diferentes")
    jogo = Jogo(
        id=str(uuid4()),
        times={time_a: 0, time_b: 0},
        status=Status.PLAYING,
    )
    _jogos[jogo.id] = jogo
    return jogo


def add_score(jogo_id: str, time: str, pontos: int) -> Jogo:
    jogo = _jogos.get(jogo_id)
    if jogo is None:
        raise KeyError(jogo_id)
    if jogo.status == Status.FINISHED:
        raise ValueError("Jogo já finalizado")
    if time not in jogo.times:
        raise ValueError(f"Time '{time}' não participa deste jogo")
    if pontos <= 0:
        raise ValueError("Pontos devem ser positivos")

    novos_times = {**jogo.times, time: jogo.times[time] + pontos}
    atualizado = jogo.model_copy(update={"times": novos_times, "status": Status.PLAYING})
    _jogos[jogo_id] = atualizado
    return atualizado


def finish_jogo(jogo_id: str) -> Jogo:
    jogo = _jogos.get(jogo_id)
    if jogo is None:
        raise KeyError(jogo_id)
    atualizado = jogo.model_copy(update={"status": Status.FINISHED})
    _jogos[jogo_id] = atualizado
    return atualizado


def reset() -> None:
    _jogos.clear()
