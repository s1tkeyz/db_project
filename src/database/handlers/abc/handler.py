from abc import ABC, abstractmethod

class DatabaseHandlerABC(ABC):
    @abstractmethod
    @staticmethod
    async def connect():
        ...

    
    @abstractmethod
    @staticmethod
    async def fetch():
        ...


    @abstractmethod
    @staticmethod
    async def execute():
        ...
