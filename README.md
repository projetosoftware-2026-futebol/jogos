# jogos

API de Jogos — microserviço em Python (FastAPI) para registrar partidas entre clubes e atualizar o placar.

## Modelo

```
JOGO
- id: str
- times: { id_clube: pontos }
- status: scheduled | playing | finished
```

## Endpoints

| Método | Rota                    | Descrição                          |
|--------|-------------------------|------------------------------------|
| GET    | `/jogos`                | Lista todos os jogos               |
| GET    | `/jogos/{id}`           | Busca um jogo pelo id              |
| GET    | `/jogos/{id}/score`     | Retorna o placar atual             |
| POST   | `/jogos/play`           | Cria um novo jogo entre dois times |
| POST   | `/jogos/{id}/score`     | Registra pontos para um time       |
| POST   | `/jogos/{id}/finish`    | Finaliza um jogo                   |
| GET    | `/health`               | Health check                       |

### Payloads

`POST /jogos/play`
```json
{ "time_a": "<id_clube_a>", "time_b": "<id_clube_b>" }
```

`POST /jogos/{id}/score`
```json
{ "time": "<id_clube>", "pontos": 1 }
```

## Como rodar

```bash
cd jogos
python -m venv .venv
. .venv/Scripts/Activate.ps1   # PowerShell
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

Documentação interativa: http://localhost:8002/docs

## Exemplos com curl

```bash
# criar partida
curl -X POST http://localhost:8002/jogos/play \
     -H "Content-Type: application/json" \
     -d '{"time_a":"flamengo","time_b":"vasco"}'

# marcar gol
curl -X POST http://localhost:8002/jogos/<id>/score \
     -H "Content-Type: application/json" \
     -d '{"time":"flamengo","pontos":1}'

# ver placar
curl http://localhost:8002/jogos/<id>/score

# finalizar
curl -X POST http://localhost:8002/jogos/<id>/finish
```

## Arquitetura

- `models.py` — schemas Pydantic (`Jogo`, `PlayRequest`, `ScoreRequest`, `Status`).
- `store.py` — estado em memória + funções puras (`create_jogo`, `add_score`, `finish_jogo`, ...).
- `main.py` — rotas FastAPI; cada handler é uma função que delega para o store.

Estilo funcional: sem classes de domínio com lógica; mutação concentrada no `store` e modelos atualizados via `model_copy`.
