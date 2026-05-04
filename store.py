"""Database store for jogos, exposed as functions.

All operations receive a database session explicitly, keeping route handlers
thin and making persistence independent from FastAPI internals.
"""
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from db_models import JogoModel
from models import Jogo


def to_schema(jogo: JogoModel) -> Jogo:
    return Jogo(id=jogo.id, times=jogo.times)


def list_jogos(db: Session) -> List[Jogo]:
    jogos = db.scalars(select(JogoModel).order_by(JogoModel.id)).all()
    return [to_schema(jogo) for jogo in jogos]


def get_jogo(db: Session, jogo_id: str) -> Optional[Jogo]:
    jogo = db.get(JogoModel, jogo_id)
    return to_schema(jogo) if jogo else None


def create_jogo(db: Session, time_a: str, pontos_a: int, time_b: str, pontos_b: int) -> Jogo:
    if time_a == time_b:
        raise ValueError("Os dois times devem ser diferentes")
    if pontos_a < 0 or pontos_b < 0:
        raise ValueError("Pontos não podem ser negativos")

    jogo = JogoModel(
        id=str(uuid4()),
        times={time_a: pontos_a, time_b: pontos_b},
    )
    db.add(jogo)
    db.commit()
    db.refresh(jogo)
    return to_schema(jogo)


def reset(db: Session) -> None:
    db.query(JogoModel).delete()
    db.commit()
