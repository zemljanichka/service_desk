import jwt
from passlib.context import CryptContext

from database import OperatorModel

ALGORITHM = "HS256"
SECRET_KEY = "ZemljanichkaServiceDesk"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def validate_operator(username: str, password: str | None = None):
    operator = await OperatorModel.get_single(OperatorModel.username == username)
    if not operator:
        return None
    if password and not verify_password(password, operator.hashed_password):
        return None
    return operator


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_token(username: str):
    return jwt.encode({"username": username}, SECRET_KEY, algorithm=ALGORITHM)
