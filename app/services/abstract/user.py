from typing import Tuple
from ...schemas.user import *
from abc import ABC, abstractmethod

class UserServiceABC(ABC):
    @abstractmethod
    async def authentificate_user(self, credentials: UserCredentials) -> int | None:
        ...
    
    @abstractmethod
    async def add_user(self, user: User) -> Tuple[bool, str]:
        ...
    
    @abstractmethod
    async def get_user_info(self, user_id: int) -> User | None:
        ...
