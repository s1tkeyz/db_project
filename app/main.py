import uvicorn
from routers.user import employee, passenger
from routers import checkin, scheduling, ticket
from fastapi import FastAPI

app = FastAPI()

app.include_router(employee.router)
app.include_router(passenger.router)
app.include_router(checkin.router)
app.include_router(scheduling.router)
app.include_router(ticket.router)