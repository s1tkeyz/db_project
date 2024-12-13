from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class Airline(BaseModel):
    name: str
    icao_code: str
    iata_code: str

class AirlineInfo(BaseModel):
    airline_id: int
    name: str

class Destination(BaseModel):
    name: str
    longitude: float
    latitude: float

class DestinationInfo(BaseModel):
    destination_id: int
    name: str

class Flight(BaseModel):
    airline_id: int
    destination_id: int
    number: int
    is_charter: bool

class FlightInfo(BaseModel):
    flight_id: int
    airline_name: str
    airline_iata: str
    flight_number: int
    destination: str

class DepartureData(BaseModel):
    flight_id: int
    scheduled_time: datetime

class Departure(BaseModel):
    flight_id: int
    scheduled_time: datetime
    actual_time: datetime
    status: str = ""
    gate: int = 0

class DepartureInfo(BaseModel):
    departure_id: int
    airline_name: str
    airline_iata: str
    flight_number: int
    scheduled_time: datetime
    destination: str

class TimetableDates(BaseModel):
    from_date: datetime
    until_date: datetime

class TimetableRow(BaseModel):
    airline_name: str
    airline_iata: str
    flight_number: int
    destination: str
    scheduled_time: datetime
    actual_time: datetime
