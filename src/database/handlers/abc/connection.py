from abc import ABC, abstractmethod
from typing import Any

class AsyncDBConnectionWrapperABC(ABC):
    """
    Database driver abstract wrapper
    """
    
    def __init__(self) -> None:
        self._connection = None

    @abstractmethod
    async def connect(self, *args, **kwargs) -> Any:
        """
        Method wrapper: connect
        """
        ...

    @abstractmethod
    async def fetch(self, *args, **kwargs) -> Any:
        """
        Method wrapper: fetch
        """
        ...

    @abstractmethod
    async def fetchrow(self, *args, **kwargs) -> Any:
        """
        Method wrapper: fetchrow
        """
        ...

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """
        Method wrapper: execute
        """
        ...

    @abstractmethod
    async def close(self, *args, **kwargs) -> None:
        """
        Method wrapper: close
        """
        ...
