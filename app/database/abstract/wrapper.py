from abc import ABC, abstractmethod
from typing import Any

class AsyncConnectionWrapperABC(ABC):
    @abstractmethod
    async def connect(self, *args, **kwargs) -> Any:
        ...
    
    @abstractmethod
    async def fetch(self, *args, **kwargs) -> Any:
        ...
    
    @abstractmethod
    async def fetchrow(self, *args, **kwargs) -> Any:
        ...
    
    @abstractmethod
    async def fetchval(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    async def close(self, *args, **kwargs) -> Any:
        ...