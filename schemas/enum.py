from enum import Enum


class Status(Enum):
    pending = "pending"
    processing = "processing"
    closed = "closed"


class Ordering(Enum):
    asc = "asc"
    desc = "desc"
