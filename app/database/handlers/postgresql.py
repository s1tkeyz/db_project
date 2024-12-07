import asyncpg
import os
from typing import Any, Dict
from .abc.connection import AsyncDBConnectionWrapperABC

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

class PosgreSQLConnectionWrapper(AsyncDBConnectionWrapperABC):
    """
    PostgreSQL connection wrapper (asyncpg driver)
    """

    def __init__(self):
        self._connection: asyncpg.Connection | None = None

    async def connect(self, *args, **kwargs) -> bool:
        try:
            self._connection = await asyncpg.connect(dsn=f"postgres://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}")
        except Exception as e:
            print(f"DB connection failed: {type(e)}")
        return self._connection is not None

    async def fetch(self, *args, **kwargs) -> Any | None:
        try:
            return await self._connection.fetch(*args, **kwargs)
        finally:
            return None

    async def fetchrow(self, *args, **kwargs) -> Any | None:
        try:
            return await self._connection.fetchrow(*args, **kwargs)
        finally:
            return None

    async def execute(self, *args, **kwargs) -> str | None:
        try:
            return await self._connection.execute(*args, **kwargs)
        finally:
            return None

    async def close(self) -> None:
        await self._connection.close()