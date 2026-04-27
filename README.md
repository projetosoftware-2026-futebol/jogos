# jogos

API de Jogos — microserviço em Python (FastAPI) para registrar partidas concluídas entre clubes.

## Modelo

```
JOGO
- id: str
- times: { id_clube: pontos }
```

Toda partida é registrada já concluída — não há estado de "em andamento".

## Endpoints

| Método | Rota                  | Descrição                                       |
|--------|-----------------------|-------------------------------------------------|
| GET    | `/jogos`              | Lista todos os jogos                            |
| GET    | `/jogos/{id}`         | Busca um jogo pelo id                           |
| GET    | `/jogos/{id}/score`   | Retorna o placar                                |
| POST   | `/jogos/play`         | Registra uma nova partida concluída             |
| GET    | `/health`             | Health check                                    |

### Payload de `POST /jogos/play`

```json
{
  "time_a": "<id_clube_a>",
  "pontos_a": 2,
  "time_b": "<id_clube_b>",
  "pontos_b": 1
}
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
# registrar partida concluída
curl -X POST http://localhost:8002/jogos/play \
     -H "Content-Type: application/json" \
     -d '{"time_a":"flamengo","pontos_a":2,"time_b":"vasco","pontos_b":1}'

# ver placar
curl http://localhost:8002/jogos/<id>/score

# listar
curl http://localhost:8002/jogos
```

## Arquitetura

- `models.py` — schemas Pydantic (`Jogo`, `PlayRequest`).
- `store.py` — estado em memória + funções puras (`create_jogo`, `list_jogos`, `get_jogo`).
- `main.py` — rotas FastAPI; cada handler é uma função que delega para o store.

Estilo funcional: sem classes de domínio com lógica; mutação concentrada no `store`.
