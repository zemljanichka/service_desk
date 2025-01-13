import datetime

from pydantic import BaseModel

from schemas import Status


class Operator(BaseModel):
    username: str
    hashed_password: str


class Assignment(BaseModel):
    ts_created: datetime.datetime
    email: str
    text: str
    operator_id: int | None = None
    status: Status = Status.pending


class OperatorResponse(BaseModel):
    id: int
    username: str
