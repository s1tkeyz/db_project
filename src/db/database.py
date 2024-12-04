import os
import asyncpg
from abc import ABC, abstractmethod

from src.schemas.flights import *
from schemas.tickets import *
from schemas.users import *

class DatabaseHandlerABC(ABC):
    ...

class PostgreSQLHandler(DatabaseHandlerABC):
    ...