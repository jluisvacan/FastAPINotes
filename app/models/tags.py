from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

# importacion para revisar tipo de datos, no en ejecucion
if TYPE_CHECKING:
    from .post import PostORM


#tabla intermedia
class TagORM(Base):
    __tablename__ = "tags"

    # Relacion uno post a muchas etiquetas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, index=True)

    posts: Mapped[List["PostORM"]] = relationship(secondary="post_tags", back_populates="tags", lazy="selectin")