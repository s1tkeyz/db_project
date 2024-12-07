from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime, timedelta
from schemas.user import *
from services.token import TokenService
from services.user.employee import EmployeeService
from services.user.passenger import PassengerService

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
    tags=["Auth", "Login"]
)

employee_service = EmployeeService()
passenger_service = PassengerService()
token_service = TokenService()

@router.get("/login")
async def passenger_login_page(request: Request):
    if await token_service.get_user_id(request.cookies.get("AccessToken")) is None:
        return templates.TemplateResponse("login.html", {"request": request})
    return RedirectResponse(url="/", status_code=302)

@router.post("/login")
async def passenger_login(request: Request, credentials: UserCredentials = Form()):
    passenger_id = await passenger_service.authentificate_user(credentials=credentials)

    if passenger_id is None:
        return JSONResponse({"message": "Error"})

    token = token_service.create_token(passenger_id, credentials.login)
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="AccessToken", value=token, max_age=datetime.now() + timedelta(hours=1))
    return response

@router.get("/signup")
async def passenger_signup_page(request: Request):
    if await token_service.get_user_id(request.cookies.get("AccessToken")) is not None:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def passenger_signup(request: Request, passenger: Passenger = Form()):
    status, msg = await passenger_service.add_user(passenger=passenger)
    return JSONResponse({"status": status, "message": msg})

@router.get("/emplogin")
async def employee_login_page(request: Request):
    if await token_service.get_user_id(request.cookies.get("AccessToken")) is None:
        return templates.TemplateResponse("emplogin.html", {"request": request})
    return RedirectResponse(url="/workplace", status_code=302)

@router.post("/emplogin")
async def employee_login(request: Request, credentials: UserCredentials = Form()):
    employee_id = await employee_service.authentificate_user(credentials=credentials)

    if employee_id is None:
        return JSONResponse({"message": "Error"})
    
    token = await token_service.create_token(employee_id, credentials.login)
    response = RedirectResponse(url="/workplace")
    response.set_cookie(key="AccessToken", value=token, max_age=datetime.now() + timedelta(hours=1))
    return response

@router.post("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(key="AccessToken")
    return response
