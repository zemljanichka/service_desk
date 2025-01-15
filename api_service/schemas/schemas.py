import datetime

from pydantic import BaseModel

from .enum import Status


class BaseModelWithId(BaseModel):
    id: int


class Operator(BaseModel):
    username: str
    hashed_password: str


class Assignment(BaseModel):
    ts_created: datetime.datetime
    email: str
    subject: str | None = None
    body: str | None = None
    operator_id: int | None = None
    status: Status = Status.pending


class AssignmentEmail(BaseModel):
    ts_created: datetime.datetime
    email: str
    subject: str | None = None
    body: str | None = None


class AssignmentWithId(BaseModelWithId, Assignment):
    pass


class OperatorResponse(BaseModelWithId):
    username: str


class TokenOut(BaseModel):
    token: str
