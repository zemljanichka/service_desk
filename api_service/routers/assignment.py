from exeptions import UnauthorizedError
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import status as status_code
from schemas import Assignment, AssignmentEmail, AssignmentWithId, Ordering, Status
from services import AssignmentService
from tasks.assignment import send_mail
from utils import authorized_user

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.get("/", response_model=list[AssignmentWithId])
async def get_assignments(status: Status = None, order_by: Ordering = None, operator=Depends(authorized_user)):
    """Получение списка обращений с фильтрацией по статусу и времени получения"""
    return await AssignmentService.get_assignments(status, order_by)


@router.post("/")
async def create(assignment: Assignment):
    """Создание обращений для теста"""
    return await AssignmentService.create_assignment(assignment.dict())


@router.post("/take")
async def take_assignment(assignment_id: int, operator=Depends(authorized_user)):
    """Присвоение обращения оператору"""
    try:
        return await AssignmentService.take_assignment(assignment_id, operator)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED, detail="Assignment already taken") from e
    except Exception as e:
        raise HTTPException(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR, detail="Assignment already taken"
        ) from e


@router.post("/send_response")
async def send_response(assignment_id: int, mail_body: str = Body(embed=True), operator=Depends(authorized_user)):
    """Отправка сообщения по обращению"""
    assignment = await AssignmentService.get_assignment_by_id(assignment_id)
    if assignment.operator_id != operator.id or assignment.status == Status.closed:
        raise HTTPException(
            status_code=status_code.HTTP_401_UNAUTHORIZED,
            detail="Assignment already taken by another operator or closed",
        )

    send_mail.send(assignment.email, assignment.subject, mail_body)


@router.post("/close_assignment")
async def close_assignment(assignment_id: int, operator=Depends(authorized_user)):
    """Закрытие обращения"""
    try:
        await AssignmentService.change_status(assignment_id, operator)
        return {"200": "OK"}
    except UnauthorizedError as e:
        raise HTTPException(status_code=status_code.HTTP_401_UNAUTHORIZED) from e
    except Exception as e:
        raise HTTPException(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR, detail="Assignment already taken"
        ) from e


@router.get("/{assignment_id}", response_model=AssignmentWithId)
async def get_assignment(assignment_id: int, operator=Depends(authorized_user)):
    """Получение обращения по id"""
    return await AssignmentService.get_assignment_by_id(assignment_id)
