from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50))

    email: Mapped[str] = mapped_column(String(100), unique=True)

    password_hash: Mapped[str] = mapped_column(String(255))
    
    tasks = relationship("Task", back_populates="user")