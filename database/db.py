import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.environ.get("POSTGRES_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


def started_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
