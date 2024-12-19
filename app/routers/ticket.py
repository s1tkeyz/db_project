from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from services.ticket import TicketService
from services.scheduling import SchedulingService
from services.token import TokenService
from schemas.ticket import *

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

scheduling_service = SchedulingService()
ticket_service = TicketService()
token_service = TokenService()

@router.post("/book")
async def book_ticket(request: Request, data: BookingData = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)

    ticket = Ticket(
        departure_id=data.departure_id,
        passenger_id=id,
        tariff_code=0,
        issue_time=datetime.now(timezone.utc),
        is_registered=False,
        service_class=data.service_class
    )
    ok, msg = await ticket_service.book_ticket(ticket)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.get("/shop")
async def get_shop_page(request: Request):
    id, _ = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/login", status_code=303)
    tickets = await scheduling_service.get_departures_pivot()
    return templates.TemplateResponse("shop.html", {
        "request": request,
        "tickets": tickets
        })
