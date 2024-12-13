from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from services.scheduling import SchedulingService
from services.token import TokenService
from schemas.scheduling import *

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

scheduling_service = SchedulingService()
token_service = TokenService()

@router.get("/timetable")
async def get_timetable_page(request: Request):
    return templates.TemplateResponse("timetable.html", {"request": request})

@router.post("/timetable")
async def get_timetable(request: Request, data: TimetableDates = Form()):
    rows = await scheduling_service.get_timetable(data.from_date, data.until_date)
    return templates.TemplateResponse("timetable.html", {
        "request": request,
        "items": rows
        })

@router.post("/add-airline")
async def add_airline(request: Request, data: Airline = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    ok, msg = await scheduling_service.add_airline(data)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.post("/add-destination")
async def add_destination(request: Request, data: Destination = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    ok, msg = await scheduling_service.add_destination(data)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.post("/add-flight")
async def add_flight(request: Request, data: Flight = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    ok, msg = await scheduling_service.add_flight(data)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.post("/add-departure")
async def add_departure(request: Request, data: DepartureData = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    
    departure = Departure(
        flight_id=data.flight_id,
        scheduled_time=data.scheduled_time,
        actual_time=data.scheduled_time
    )
    ok, msg = await scheduling_service.add_departure(departure)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })
