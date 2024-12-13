from datetime import date
from schemas.scheduling import *
from abc import ABC, abstractmethod

class SchedulingServiceABC(ABC):
    @abstractmethod
    async def add_airline(self, airline: Airline) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def add_destination(self, destination: Destination) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def add_flight(self, flight: Flight) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def add_departure(self, departure: Departure) -> tuple[bool, str]:
        ...
    
    @abstractmethod
    async def update_departure(self, departure_id: int, data: Departure) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def get_departures(self, skip=0, limit=10) -> list[Departure] | None:
        ...

    @abstractmethod
    async def get_timetable(self, from_date: date, until_date: date) -> list[TimetableRow] | None:
        ...
