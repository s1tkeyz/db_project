from typing import Literal
from pydantic import BaseModel, Field
from datetime import date, datetime

class Airline(BaseModel):
    airline_id: int = Field(..., title="Airline ID")
    icao_code: str = Field(..., title="Airline ICAO code", max_length=3)
    iata_code: str = Field(..., title="Airline IATA code", max_length=2)
    name: str = Field(..., title="Airline name", max_length=32)

class Destination(BaseModel):
    destination_id: int = Field(..., title="Destination ID")
    name: str = Field(..., title="Destination name", max_length=32)

class Flight(BaseModel):
    flight_id: int = Field(..., title="Flight ID")
    airline_id: int = Field(..., title="Airline ID")
    destination_id: int = Field(..., title="Destination ID")
    number: int = Field(..., title="Flight number")
    is_charter: bool = Field(..., title="Charter flag")

class Departure(BaseModel):
    departure_id: int = Field(..., title="Departure ID")
    flight_id: int = Field(..., title="Flight ID")
    scheduled_time: datetime = Field(..., title="Scheduled departure time")
    actual_time: datetime = Field(..., title="Actual departure time")
    gate: int = Field(..., title="Boarding gate number")
    departed: bool = Field(..., title="Departure flag")