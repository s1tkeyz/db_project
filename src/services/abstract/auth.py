from abc import ABC, abstractmethod
from ...schemas.auth import *
from typing import Tuple

class AuthServiceABC(ABC):
    @abstractmethod
    async def check_user(self, credentials: UserCredentials) -> int | None:
        ...

    @abstractmethod
    async def add_user(self, credentials: UserCredentials) -> Tuple[bool, str]:
        ...
    
    @abstractmethod
    async def remove_user(self, user_id: int) -> Tuple[bool, str]:
        ...