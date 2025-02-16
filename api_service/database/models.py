from database.db import SessionLocal
from schemas import Status
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, select
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    @classmethod
    async def get_single(cls, *filter):
        return SessionLocal().scalar(select(cls).where(*filter))

    @classmethod
    async def select(cls, *filter, order_by=None):
        query = select(cls).where(*filter)
        if order_by is not None:
            query = query.order_by(order_by)
        return SessionLocal().scalars(query).all()

    @classmethod
    async def insert(cls, **kwargs):
        session = SessionLocal()
        new_obj = cls(**kwargs)
        session.add(new_obj)
        session.commit()
        session.refresh(new_obj)
        return new_obj

    @classmethod
    async def delete(cls, *filter):
        session = SessionLocal()
        session.query(cls).filter(*filter).delete()
        session.commit()

    @classmethod
    async def update(cls, *filter, update_data):
        session = SessionLocal()
        session.query(cls).filter(*filter).update(update_data)
        session.commit()


class Assignment(BaseModel):
    __tablename__ = "assignment"

    ts_created = Column(DateTime, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    body = Column(String, nullable=True)
    operator_id = Column(Integer, ForeignKey("operator.id"), nullable=True, default=None)
    status: Status = Column(Enum(Status), default=Status.pending)


class Operator(BaseModel):
    __tablename__ = "operator"

    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
