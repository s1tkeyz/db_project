from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from services.checkin import CheckInService
from services.token import TokenService
from schemas.checkin import *

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

checkin_service = CheckInService()
token_service = TokenService()

@router.post("/checkin")
async def checkin_passenger(request: Request, data: CheckInData = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)       
    
    ok, msg, bp = await checkin_service.checkin_passenger(data)
    return JSONResponse({
        "status": ok,
        "message": msg,
        "bp_id": bp[0],
        "seat": bp[1]
    })