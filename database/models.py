from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from database.db import SessionLocal


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class Assignment(BaseModel):
    __tablename__ = "assignment"

    ts_created = Column(DateTime, nullable=False)
    email = Column(String, nullable=False)
    text = Column(String, nullable=False)
    operator_id = Column(Integer, ForeignKey("operator.id"), nullable=True, default=None)
    status = Column(String, nullable=False)


class Operator(BaseModel):
    __tablename__ = "operator"

    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
