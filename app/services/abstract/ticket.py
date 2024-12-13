from schemas.ticket import *
from abc import ABC, abstractmethod

class TicketServiceABC(ABC):
    @abstractmethod
    async def book_ticket(self, data: BookingData) -> tuple[bool, str]:
        ...
