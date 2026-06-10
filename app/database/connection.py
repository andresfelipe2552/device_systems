from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./device_systems.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Solo necesario para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    """Crea todas las tablas en la base de datos."""
    from app.models import user_model  # noqa: F401 — necesario para registrar el modelo
    Base.metadata.create_all(bind=engine)
