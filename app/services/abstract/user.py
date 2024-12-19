from schemas.user import *
from abc import ABC, abstractmethod

class UserServiceABC(ABC):
    @abstractmethod
    async def auth_user(self, credentials: UserCredentials) -> int | None:
        ...

    @abstractmethod
    async def add_user(self, user: User) -> tuple[bool, str]:
        ...
    
    @abstractmethod
    async def remove_user(self, user_id: int) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def get_user_info(self, user_id: int) -> User:
        ...
    
    @abstractmethod
    async def edit_user(self, user_id: int, user: User) -> tuple[bool, str]:
        ...

    @abstractmethod
    async def get_users(self) -> list[User]:
        ...
