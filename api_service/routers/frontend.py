from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import status as status_code
from schemas import Assignment, AssignmentEmail, Ordering, Status
from services import AssignmentService, OperatorService
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from tasks.assignment import send_mail
from utils import authorized_user, validate_operator

router = APIRouter(prefix="/frontend", tags=["frontend"])

templates = Jinja2Templates(directory="html_templates")


@router.get("/")
async def get_start_html(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@router.get("/assignments")
async def get_assignments(request: Request):
    return templates.TemplateResponse("main_page.html", context={"request": request})


@router.get("/assignments/{assignment_id}")
async def get_assignment(request: Request, assignment_id: int):
    return templates.TemplateResponse("assignment.html", context={"request": request, "id": assignment_id})
