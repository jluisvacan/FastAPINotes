from datetime import datetime
from typing import Literal, List

from sqlalchemy import String, Enum, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.post import PostORM

Role = Literal["user","editor","admin"]

class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index= True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(500), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum("user", "editor","admin", name="role_enum"), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    create_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.now )

    posts: Mapped[List["PostORM"]] = relationship(back_populates="user")