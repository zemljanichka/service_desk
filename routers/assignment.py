from fastapi import APIRouter

router = APIRouter(prefix="/assignment", tags=["assignment"])


@router.get("/")
async def get_assignments():
    pass


@router.post("/take")
async def take_assignment(assignment_id: int):
    pass


@router.post("/send_response")
async def send_response(assignment_id: int):
    pass
