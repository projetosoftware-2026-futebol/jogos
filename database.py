import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


def get_database_url() -> str:
    db_user = os.getenv("MYSQL_USER", "root")
    db_password = os.getenv("MYSQL_PASSWORD", "football-password")
    db_host = os.getenv("MYSQL_HOST", "localhost")
    db_port = os.getenv("MYSQL_PORT", "3306")
    db_name = os.getenv("MYSQL_DATABASE", "football")

    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
