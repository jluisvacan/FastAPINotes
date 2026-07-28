from __future__ import annotations
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, UniqueConstraint, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

# importacion para revisar tipo de datos, no en ejecucion
if TYPE_CHECKING:
    from .user import UserORM
    from .tags import TagORM
    from .category import CategoryORM

#tabla intermedia para relacion muchos a muchos
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True ),
        Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True )
)

#Clase que representa la tabla post en SQLAlchemist
class PostORM(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("title", name="posts_unique"),)
    #Mapped define el tipo de dato que tiene la columna
    #mapped_column permite definir los detalles del atributo
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(300), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #Llave foranea
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped[Optional["UserORM"]] = relationship(back_populates="posts")

    category_id: Mapped[Optional[str]] = mapped_column(ForeignKey("category.id", ondelete="SET NULL"), nullable=True, index=True)
    category = relationship("CategoryORM", back_populates="posts")

    tags: Mapped[List["TagORM"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
        lazy="selectin",
        passive_deletes=True
    )