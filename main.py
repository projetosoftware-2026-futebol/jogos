"""API de Jogos.

Endpoints:
    GET  /jogos              -> lista todos os jogos
    GET  /jogos/{id}         -> obtém um jogo
    GET  /jogos/{id}/score   -> placar do jogo
    POST /jogos/play         -> registra um novo jogo (já concluído) entre dois times
"""
from fastapi import FastAPI, HTTPException
from typing import Dict, List

import store
from models import Jogo, PlayRequest


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
    return {"id": jogo.id, "times": jogo.times}


@app.post("/jogos/play", response_model=Jogo, status_code=201)
def play(req: PlayRequest) -> Jogo:
    try:
        return store.create_jogo(req.time_a, req.pontos_a, req.time_b, req.pontos_b)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}
