from typing import Literal
from pydantic import BaseModel, Field
from datetime import date

class Ticket(BaseModel):
    ticket_id: int = Field(..., title="Ticket ID")
    departure_id: int = Field(..., title="Departure ID")
    passenger_id: int = Field(..., title="Passenger ID")
    tariff_code: int = Field(..., title="Internal tariff code")
    service_class: Literal['Y', 'C'] = Field(..., title="Ticket service class")

class BoardingPass(BaseModel):
    bp_id: int = Field(..., title="Boarding pass ID")
    ticket_id: int = Field(..., title="Ticket ID")
    has_luggage: int = Field(..., title="Luggage flag")
    seat: str = Field(..., title="Seat")

class LuggagePass(BaseModel):
    luggage_id: int = Field(..., title="Luggage pass ID")
    weight: float = Field(..., title="Luggage weight")
    description: str = Field(..., title="Luggage short description")