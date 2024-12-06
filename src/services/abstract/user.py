from abc import ABC, abstractmethod
from ...schemas.user import *
from typing import Tuple

class UserService(ABC):
    @abstractmethod
    async def add_user(user: User) -> Tuple[bool, int]:
        ...

    @abstractmethod
    async def get_user_info(user_id: int) -> User:
        ...
    
    @abstractmethod
    async def update_user_info(user_id: int) -> Tuple[bool, int]:
        ...