from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi import status as status_code
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from schemas import Assignment, Ordering, Status, AssignmentEmail
from services import AssignmentService, OperatorService
from utils import authorized_user, validate_operator
from tasks.assignment import send_mail

router = APIRouter(prefix="/frontend", tags=["frontend"])

templates = Jinja2Templates(directory="html_templates")


@router.get("/")
async def get_start_html(request: Request):
    return templates.TemplateResponse("login.html", context={'request': request})


@router.get("/assignments")
async def get_assignments(request: Request):
    return templates.TemplateResponse("main_page.html", context={'request': request})


@router.get("/assignments/{assignment_id}")
async def get_assignment(request: Request, assignment_id: int):
    return templates.TemplateResponse("assignment.html", context={'request': request, 'id': assignment_id})
