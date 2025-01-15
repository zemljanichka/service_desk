import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "POSTGRES_URL", "postgresql+psycopg2://test_postgres:test_postgres@localhost:5434/test_db"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


def started_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
