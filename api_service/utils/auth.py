import jwt
from database import OperatorModel
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET_KEY = "ZemljanichkaServiceDesk"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def validate_operator(username: str, password: str | None = None):
    """Проверка данных оператора"""
    operator = await OperatorModel.get_single(OperatorModel.username == username)
    if not operator:
        return None
    if password and not verify_password(password, operator.hashed_password):
        return None
    return operator


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def generate_token(username: str):
    return jwt.encode({"username": username}, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
