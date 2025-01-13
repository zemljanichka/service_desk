from fastapi import APIRouter, Depends

from schemas import Assignment, Ordering, Status
from services import AssignmentService
from utils import authorized_user

router = APIRouter(prefix="/assignment", tags=["assignment"])


@router.get("/")
async def get_assignments(status: Status = None, order_by: Ordering = None, operator=Depends(authorized_user)):
    return await AssignmentService.get_assignments(status, order_by)


@router.post("/")
async def create_invocation(assignment_data: Assignment):
    return await AssignmentService.create_assignment(assignment_data)


@router.post("/take")
async def take_assignment(assignment_id: int, operator=Depends(authorized_user)):
    return await AssignmentService.take_assignment(assignment_id, operator)


@router.post("/send_response")
async def send_response(assignment_id: int):
    pass
