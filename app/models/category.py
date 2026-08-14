from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.core.db import Base
from app.models.post import PostORM


class CategoryORM(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index= True)
    name: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(60), unique=True, index=True)

    #relacion con los Posts
    posts = relationship("PostORM", back_populates="category", cascade="all, delete", passive_deletes=True)
