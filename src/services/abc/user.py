from abc import ABC, abstractmethod
from ...schemas.users import *
from typing import Tuple
from passlib.context import CryptContext

class UserServiceABC(ABC):
    def __init__(self) -> None:
        self._crypt_ctx = None

    @abstractmethod
    async def authentificate_user(self, login: str, password: str) -> Tuple[bool, str]:
        """
        Authentificate user in system
        """
        ...

    @abstractmethod
    async def add_new_user(self, userdata: User) -> Tuple[bool, str]:
        """
        Add new user to the system
        """
        ...
    
    @abstractmethod
    async def remove_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Remove user from the system by user_id
        """
        ...

    @abstractmethod
    async def get_user_info(self, user_id: int) -> User | None:
        """
        Get user info by user_id
        """
        ...

    @abstractmethod
    async def update_user(self, user_id: int, userdata: User) -> Tuple[bool, str]:
        """
        Updates user info by user_id
        """
        ...
