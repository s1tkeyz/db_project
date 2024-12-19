from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from services.user.passenger import PassengerService
from services.token import TokenService
from schemas.user import *

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

passenger_service = PassengerService()
token_service = TokenService()

@router.get("/login")
async def get_login_page(request: Request):
    id, _ = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return templates.TemplateResponse("login.html", {"request": request})
    return RedirectResponse(url="/timetable", status_code=302)

@router.post("/login")
async def login(request: Request, credentials: UserCredentials = Form()):
    id, _ = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id:
        return RedirectResponse(url="/timetable", status_code=303)
    id = await passenger_service.auth_user(credentials=credentials)
    if id is None:
        return JSONResponse({
            "status": False,
            "message": "Invalid credentials"
        })
    token = await token_service.create_token(id, credentials.login, False)
    response = JSONResponse({
        "status": True,
        "message": "Logged in"
    })
    response.set_cookie(key="AccessToken", value=token, max_age=datetime.now(timezone.utc) + timedelta(hours=1))
    return response

@router.get("/signup")
async def get_signup_page(request: Request):
    id, _ = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id:
        return RedirectResponse(url="/timetable", status_code=302)
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def signup(request: Request, data : Passenger = Form()):
    ok, msg = await passenger_service.add_user(data)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.post("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(key="AccessToken")
    return response
