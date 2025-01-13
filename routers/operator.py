from fastapi import APIRouter


router = APIRouter(prefix="/operator", tags=["operator"])

@router.post("/login")
async def login_operator(username: str, password: str):
    pass


@router.get("/me")
async def get_operator_data():
    pass