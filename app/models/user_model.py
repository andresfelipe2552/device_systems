from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime
from app.database.connection import Base


class User(Base):
    """Modelo SQLAlchemy que representa la tabla 'users' en la base de datos."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} role={self.role!r}>"
