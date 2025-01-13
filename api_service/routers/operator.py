from fastapi import APIRouter, Depends, HTTPException

from services import OperatorService
from utils import authorized_user, validate_operator

router = APIRouter(prefix="/operator", tags=["operator"])


@router.post("/login")
async def login_operator(username: str, password: str):
    if not await validate_operator(username, password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return await OperatorService.get_token(username)


@router.get("/me")
async def get_operator_data(operator=Depends(authorized_user)):
    return operator
