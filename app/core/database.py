"""Database engine and session helpers."""

from collections.abc import Generator
import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import DATABASE_URL


class Base(DeclarativeBase):
    """Base class for all database models."""


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

if all((DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)):
    database_url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )
else:
    database_url = DATABASE_URL

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session]:
    """Provide a database session for one API request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
