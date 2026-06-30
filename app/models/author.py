from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

# importacion para revisar tipo de datos, no en ejecucion
if TYPE_CHECKING:
    from .post import PostORM

#Clase que representa la tabla authors en SQLAlchemist
class AuthorORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100),unique=True, index=True)

    # relacion con tabla POST. relacion uno (autor) a muchos (posts)
    posts: Mapped[List["PostORM"]] = relationship(back_populates="author")