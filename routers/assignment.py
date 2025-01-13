from fastapi import APIRouter

from schemas import Assignment
from services import AssignmentService

router = APIRouter(prefix="/assignment", tags=["assignment"])


@router.get("/")
async def get_assignments():
    return await AssignmentService.get_assignments()


@router.post("/")
async def create_invocation(assignment_data: Assignment):
    return await AssignmentService.create_assignment(assignment_data)


@router.post("/take")
async def take_assignment(assignment_id: int, operator_id: int):
    return await AssignmentService.take_assignment(assignment_id, operator_id)


@router.post("/send_response")
async def send_response(assignment_id: int):
    pass
