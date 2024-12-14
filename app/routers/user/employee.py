from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from services.checkin import CheckInService
from services.ticket import TicketService
from services.user.employee import EmployeeService
from services.user.passenger import PassengerService
from services.scheduling import SchedulingService
from services.token import TokenService
from schemas.user import *
from schemas.scheduling import *
from schemas.checkin import *
from schemas.ticket import *

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

checkin_service = CheckInService()
scheduling_service = SchedulingService()
passenger_service = PassengerService()
employee_service = EmployeeService()
ticket_service = TicketService()
token_service = TokenService()

@router.get("/emplogin")
async def get_employee_login_page(request: Request):
    id, _ =  await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return templates.TemplateResponse("emplogin.html", {"request": request})
    return RedirectResponse(url="/workplace")

@router.post("/emplogin")
async def employee_login(request: Request, credentials: UserCredentials = Form()):
    id = await employee_service.auth_user(credentials=credentials)
    if id is None:
        return JSONResponse({"message": "Invalid credentials"})
    token = await token_service.create_token(id, credentials.login, True)
    response = RedirectResponse(url="/workplace", status_code=303)
    response.set_cookie(key="AccessToken", value=token, max_age=datetime.now(timezone.utc) + timedelta(hours=1))
    return response

@router.get("/workplace")
async def get_workplace_page(request: Request):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if (id is None) or (not emp):
        return RedirectResponse(url="/emplogin", status_code=303)
    if await employee_service.is_super(employee_id=id):
        airlines = await scheduling_service.get_airlines_list()
        destinations = await scheduling_service.get_destinations_list()
        flights = await scheduling_service.get_flights_pivot()
        return templates.TemplateResponse("dashboard.html", {
                                            "request": request,
                                            "airlines": airlines,
                                            "destinations": destinations,
                                            "flights": flights})
    return templates.TemplateResponse("checkin.html", {"request": request})

@router.post("/add-employee")
async def add_employee(request: Request, data: Employee = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if (id is None) or (not emp):
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    ok, msg = await employee_service.add_user(data)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

@router.post("/remove-employee")
async def remove_employee(request: Request, employee_id: int = Form()):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)
    ok, msg = await employee_service.remove_user(employee_id)
    if ok:
        return RedirectResponse(url="/workplace", status_code=303)
    return JSONResponse({
        "status": ok,
        "message": msg
    })

router.get("/tableview/{table_name:path}")
async def table_view(table_name: str, request: Request):
    id, emp = await token_service.get_user_info(request.cookies.get("AccessToken"))
    if id is None:
        return RedirectResponse(url="/emplogin", status_code=303)
    if not emp:
        return JSONResponse({
            "status": False,
            "message": "Forbidden"
        }, status_code=403)

    columns = None
    rows = None

    if table_name == "employees":
        data = await employee_service.get_users()
        rows = [d.model_dump().values() for d in data]
        columns = Employee.model_fields.keys()
    elif table_name == "passengers":
        data = await passenger_service.get_users()
        rows = [d.model_dump().values() for d in data]
        columns = Passenger.model_fields.keys()
    elif table_name == "airlines":
        data = await scheduling_service.get_airlines()
        rows = [d.model_dump().values() for d in data]
        columns = Airline.model_fields.keys()
    elif table_name == "destinations":
        data = await scheduling_service.get_destinations_list()
        rows = [d.model_dump().values() for d in data]
        columns = DestinationInfo.model_fields.keys()
    elif table_name == "flights":
        data = await scheduling_service.get_flights_pivot()
        rows = [d.model_dump().values() for d in data]
        columns = FlightInfo.model_fields.keys()
    elif table_name == "departures":
        data = await scheduling_service.get_departures()
        rows = [d.model_dump().values() for d in data]
        columns = Departure.model_fields.keys()
    elif table_name == "bp":
        data = await checkin_service.get_bp()
        rows = [d.model_dump().values() for d in data]
        columns = BoardingPass.model_fields.keys()
    elif table_name == "tickets":
        data = await ticket_service.get_tickets()
        rows = [d.model_dump().values() for d in data]
        columns = Ticket.model_fields.keys()
    else:
        return JSONResponse({
            "status": False,
            "message": "Unknown table name"
        })
    return templates.TemplateResponse(
        "tableview.html",
        {
            "request": request,
            "columns": columns,
            "rows": rows,
            "dbname": table_name
        }
    )