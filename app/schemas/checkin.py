from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class BoardingPass(BaseModel):
    ticket_id: int
    has_luggage: bool
    seat: str
    issue_time: datetime

class CheckInData(BaseModel):
    airline_name: str
    flight_number: int
    destination: str
    passenger_name: str
    passenger_surname: str
    passport_number: str
