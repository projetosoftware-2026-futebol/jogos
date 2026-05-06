from sqlalchemy.orm import Session

import store
from database import get_database_url, get_db


# -- Sistema ------------------------------------------------------------------

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_db_entrega_sessao():
    generator = get_db()
    db = next(generator)

    assert isinstance(db, Session)

    generator.close()


def test_get_database_url_usa_variaveis_de_ambiente(monkeypatch):
    monkeypatch.setenv("MYSQL_USER", "user")
    monkeypatch.setenv("MYSQL_PASSWORD", "pass")
    monkeypatch.setenv("MYSQL_HOST", "db")
    monkeypatch.setenv("MYSQL_PORT", "3307")
    monkeypatch.setenv("MYSQL_DATABASE", "fut")

    assert get_database_url() == "mysql+pymysql://user:pass@db:3307/fut"


# -- Jogos --------------------------------------------------------------------

def test_lista_todos_os_jogos(client):
    response = client.get("/jogos")

    assert response.status_code == 200
    jogos = response.json()
    assert len(jogos) == 2
    assert jogos[0] == {"id": "jogo-1", "times": {"palmeiras": 2, "santos": 1}}
    assert jogos[1]["times"] == {"flamengo": 0, "vasco": 0}


def test_lista_jogos_rota_antiga_zambom(client):
    response = client.get("/jogos/zambom")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_obtem_jogo_por_id(client):
    response = client.get("/jogos/jogo-1")

    assert response.status_code == 200
    jogo = response.json()
    assert jogo["id"] == "jogo-1"
    assert jogo["times"] == {"palmeiras": 2, "santos": 1}


def test_jogo_inexistente_retorna_404(client):
    response = client.get("/jogos/nao-existe")

    assert response.status_code == 404
    assert "encontrado" in response.json()["detail"]


def test_obtem_placar_do_jogo(client):
    response = client.get("/jogos/jogo-2/score")

    assert response.status_code == 200
    assert response.json() == {
        "id": "jogo-2",
        "times": {"flamengo": 0, "vasco": 0},
    }


def test_placar_de_jogo_inexistente_retorna_404(client):
    response = client.get("/jogos/nao-existe/score")

    assert response.status_code == 404
    assert "encontrado" in response.json()["detail"]


# -- Play ---------------------------------------------------------------------

def test_cria_jogo_e_consegue_buscar(client):
    create_response = client.post(
        "/jogos/play",
        json={
            "time_a": "corinthians",
            "pontos_a": 3,
            "time_b": "sao-paulo",
            "pontos_b": 2,
        },
    )
    assert create_response.status_code == 201

    created = create_response.json()
    assert "id" in created
    assert created["times"] == {"corinthians": 3, "sao-paulo": 2}

    get_response = client.get(f"/jogos/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == created


def test_cria_jogo_com_pontuacao_padrao(client):
    response = client.post(
        "/jogos/play",
        json={"time_a": "botafogo", "time_b": "gremio"},
    )

    assert response.status_code == 201
    assert response.json()["times"] == {"botafogo": 0, "gremio": 0}


def test_nao_cria_jogo_com_times_iguais(client):
    response = client.post(
        "/jogos/play",
        json={"time_a": "bahia", "pontos_a": 1, "time_b": "bahia", "pontos_b": 2},
    )

    assert response.status_code == 400
    assert "diferentes" in response.json()["detail"]


def test_nao_cria_jogo_com_pontos_negativos(client):
    response = client.post(
        "/jogos/play",
        json={"time_a": "sport", "pontos_a": -1, "time_b": "vitoria", "pontos_b": 0},
    )

    assert response.status_code == 400
    assert "negativos" in response.json()["detail"]


def test_reset_store_remove_jogos(db_session):
    assert len(store.list_jogos(db_session)) == 2

    store.reset(db_session)

    assert store.list_jogos(db_session) == []
