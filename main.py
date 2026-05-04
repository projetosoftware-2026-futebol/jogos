"""API de Jogos.

Endpoints:
    GET  /jogos              -> lista todos os jogos
    GET  /jogos/{id}         -> obtém um jogo
    GET  /jogos/{id}/score   -> placar do jogo
    POST /jogos/play         -> registra um novo jogo (já concluído) entre dois times
"""
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import store
from database import Base, engine, get_db
from models import Jogo, PlayRequest


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Jogos API", version="1.0.0", lifespan=lifespan)


@app.get("/jogos", response_model=List[Jogo])
def listar(db: Session = Depends(get_db)) -> List[Jogo]:
    return store.list_jogos(db)


@app.get("/jogos/{jogo_id}", response_model=Jogo)
def obter(jogo_id: str, db: Session = Depends(get_db)) -> Jogo:
    jogo = store.get_jogo(db, jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo


@app.get("/jogos/{jogo_id}/score")
def placar(jogo_id: str, db: Session = Depends(get_db)) -> Dict[str, object]:
    jogo = store.get_jogo(db, jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return {"id": jogo.id, "times": jogo.times}


@app.post("/jogos/play", response_model=Jogo, status_code=201)
def play(req: PlayRequest, db: Session = Depends(get_db)) -> Jogo:
    try:
        return store.create_jogo(db, req.time_a, req.pontos_a, req.time_b, req.pontos_b)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}
