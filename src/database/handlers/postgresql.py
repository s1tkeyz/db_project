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

    async def connect(self, *args, **kwargs) -> bool:
        try:
            self._connection = await asyncpg.connect(**DB_CONFIG)
        except ConnectionError as e:
            pass
        return self._connection is None

    async def fetch(self, query: str, *query_params) -> Any | None:
        try:
            return await self._connection.fetch(query=query, *query_params)
        finally:
            return None

    async def fetchrow(self, query: str, *query_params) -> Any | None:
        try:
            return await self._connection.fetchrow(query=query, *query_params)
        finally:
            return None

    async def execute(self, query: str, *query_params) -> str | None:
        try:
            return await self._connection.execute(query=query, *query_params)
        finally:
            return None

    async def close(self) -> None:
        await self._connection.close()