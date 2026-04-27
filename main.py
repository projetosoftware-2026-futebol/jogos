"""API de Jogos.

Endpoints:
    GET  /jogos              -> lista todos os jogos
    GET  /jogos/{id}         -> obtém um jogo
    GET  /jogos/{id}/score   -> placar atual do jogo
    POST /jogos/play         -> cria um novo jogo entre dois times
    POST /jogos/{id}/score   -> registra pontos para um time
    POST /jogos/{id}/finish  -> finaliza um jogo
"""
from fastapi import FastAPI, HTTPException
from typing import Dict, List

import store
from models import Jogo, PlayRequest, ScoreRequest


app = FastAPI(title="Jogos API", version="1.0.0")


@app.get("/jogos", response_model=List[Jogo])
def listar() -> List[Jogo]:
    return store.list_jogos()


@app.get("/jogos/{jogo_id}", response_model=Jogo)
def obter(jogo_id: str) -> Jogo:
    jogo = store.get_jogo(jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo


@app.get("/jogos/{jogo_id}/score")
def placar(jogo_id: str) -> Dict[str, object]:
    jogo = store.get_jogo(jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return {"id": jogo.id, "status": jogo.status, "times": jogo.times}


@app.post("/jogos/play", response_model=Jogo, status_code=201)
def play(req: PlayRequest) -> Jogo:
    try:
        return store.create_jogo(req.time_a, req.time_b)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/jogos/{jogo_id}/score", response_model=Jogo)
def marcar(jogo_id: str, req: ScoreRequest) -> Jogo:
    try:
        return store.add_score(jogo_id, req.time, req.pontos)
    except KeyError:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/jogos/{jogo_id}/finish", response_model=Jogo)
def finalizar(jogo_id: str) -> Jogo:
    try:
        return store.finish_jogo(jogo_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}
