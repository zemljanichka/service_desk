from fastapi import APIRouter, Depends, Body

from schemas import Assignment, Ordering, Status, AssignmentEmail
from services import AssignmentService
from utils import authorized_user
from tasks.assignment import send_mail

router = APIRouter(prefix="/assignment", tags=["assignment"])


@router.get("/")
async def get_assignments(status: Status = None, order_by: Ordering = None, operator=Depends(authorized_user)):
    return await AssignmentService.get_assignments(status, order_by)


@router.post("/take")
async def take_assignment(assignment_id: int, operator=Depends(authorized_user)):
    return await AssignmentService.take_assignment(assignment_id, operator)


@router.post("/send_response")
async def send_response(assignment_id: int, mail_body: str = Body(), operator=Depends(authorized_user)):
    assignment = await AssignmentService.get_assignment_by_id(assignment_id)
    if assignment.operator_id != operator.id or assignment.status == Status.closed:
        raise Exception

    send_mail.send(assignment.email, assignment.subject, mail_body)


@router.post("/close_assignment")
async def close_assignment(assignment_id: int, operator=Depends(authorized_user)):
    return await AssignmentService.change_status(assignment_id, operator)

