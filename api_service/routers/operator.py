from database import OperatorModel
from fastapi import APIRouter, Body, Depends, HTTPException, status
from schemas import Operator, OperatorResponse, TokenOut
from services import OperatorService
from utils import authorized_user, hash_password, validate_operator

router = APIRouter(prefix="/operator", tags=["operator"])


@router.post("/")
async def create(operator: Operator):
    await OperatorModel.insert(username=operator.username, hashed_password=hash_password(operator.hashed_password))


@router.post("/login", response_model=TokenOut)
async def login_operator(username: str = Body(), password: str = Body()):
    """Авторизация оператора, получение токена"""
    if not await validate_operator(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return await OperatorService.get_token(username)


@router.get("/me", response_model=OperatorResponse)
async def get_operator_data(operator=Depends(authorized_user)):
    """Получение данных оператора по токену"""
    return operator
