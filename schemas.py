import datetime
from enum import Enum

from pydantic import BaseModel


class Status(Enum):
    pending = "pending"
    processing = "processing"
    closed = "closed"


class Operator(BaseModel):
    username: str
    hashed_password: str


class Assignment(BaseModel):
    ts_created: datetime.datetime
    email: str
    text: str
    operator_id: int | None = None
    status: Status = Status.pending
