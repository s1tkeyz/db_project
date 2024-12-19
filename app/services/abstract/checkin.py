from schemas.checkin import *
from abc import ABC, abstractmethod

class CheckInServiceABC(ABC):
    @abstractmethod
    async def checkin_passenger(self, data: CheckInData) -> tuple[bool, str, tuple[int, str]]:
        ...

    @abstractmethod
    async def get_bp(self) -> list[BoardingPass]:
        ...