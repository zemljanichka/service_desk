from fastapi import Header, HTTPException

from schemas import OperatorResponse
from utils.auth import decode_token, validate_operator


async def authorized_user(token: str = Header(...)) -> OperatorResponse:
    try:
        username = decode_token(token)["username"]
        operator = await validate_operator(username)
        if not operator:
            raise Exception
        return operator
    except Exception as e:
        raise HTTPException(status_code=402, detail="Incorrect token") from e
