import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from database import Base, get_db
from db_models import JogoModel


def jogos_para_teste() -> list[JogoModel]:
    return [
        JogoModel(id="jogo-1", times={"palmeiras": 2, "santos": 1}),
        JogoModel(id="jogo-2", times={"flamengo": 0, "vasco": 0}),
    ]


@pytest.fixture
def app():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    original_engine = main.engine

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    main.engine = engine
    Base.metadata.create_all(bind=engine)
    with testing_session_local() as db:
        db.add_all(jogos_para_teste())
        db.commit()

    main.app.dependency_overrides[get_db] = override_get_db
    main.app.state.testing_session_local = testing_session_local
    yield main.app
    main.app.dependency_overrides.pop(get_db, None)
    Base.metadata.drop_all(bind=engine)
    main.engine = original_engine


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session(app):
    db = app.state.testing_session_local()
    try:
        yield db
    finally:
        db.close()
