from abc import ABC, abstractmethod

class AuthServiceABC(ABC):
    @abstractmethod
    async def create_access_token():
        ...

    @abstractmethod
    async def get_current_user():
        ...

    @abstractmethod
    async def authentificate_user():
        ...
