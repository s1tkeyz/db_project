from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class BookingData(BaseModel):
    departure_id: int
    service_class: Literal['Y', 'C']

class Ticket(BaseModel):
    departure_id: int
    passenger_id: int
    tariff_code: int
    issue_time: datetime
    is_registered: bool
    service_class: Literal['Y', 'C']