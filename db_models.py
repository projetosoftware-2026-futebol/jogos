from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class JogoModel(Base):
    __tablename__ = "jogos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    times: Mapped[dict[str, int]] = mapped_column(JSON, nullable=False)
