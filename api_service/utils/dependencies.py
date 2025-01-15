from fastapi import Header, HTTPException, status

from schemas import OperatorResponse
from .auth import decode_token, validate_operator


async def authorized_user(token: str = Header(...)) -> OperatorResponse:
    """Проверка токена пользователя"""
    try:
        username = decode_token(token)["username"]
        operator = await validate_operator(username)
        if not operator:
            raise Exception
        return operator
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token") from e
