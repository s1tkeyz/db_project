import os
import logging
import asyncpg
from typing import Any, Literal
from database.abstract.wrapper import AsyncConnectionWrapperABC


logger = logging.getLogger(__name__)

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": 5432 #os.getenv("DB_PORT"),
}

DB_RO_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_RO_USER"),
    "password": os.getenv("DB_RO_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

class AsyncpgConnectionWrapper(AsyncConnectionWrapperABC):
    def __init__(self, mode: Literal["admin", "readonly"] = "admin"):
        self._conn: asyncpg.Connection | None = None
        if mode == "readonly":
            self._config = DB_RO_CONFIG
        else:
            self._config = DB_CONFIG
    
    async def connect(self, *args, **kwargs) -> bool:
        if self._conn is not None:
            logger.log("Already connected")
            return False
    
        try:
            self._conn = await asyncpg.connect(**self._config)
            logger.info("Successfully connected to DB")
            return True
        except Exception as e:
            print(f"Failed database connection: {e}")
            return False
    
    async def fetch(self, *args, **kwargs) -> Any:
        try:
            return await self._conn.fetch(*args, **kwargs)
        except Exception as e:
            logger.info(f"Failed fetch(...) call: {e}")
            return None
    
    async def fetchrow(self, *args, **kwargs) -> Any:
        try:
            return await self._conn.fetchrow(*args, **kwargs)
        except Exception as e:
            logger.info(f"Failed fetchrow(...) call: {e}")
            return None
    
    async def fetchval(self, *args, **kwargs) -> Any:
        try:
            return await self._conn.fetchval(*args, **kwargs)
        except Exception as e:
            logger.info(f"Failed fetchval(...) call: {e}")
            return None

    async def execute(self, *args, **kwargs) -> Any:
        try:
            return await self._conn.execute(*args, **kwargs)
        except Exception as e:
            logger.info(f"Failed execute(...) call: {e}")
            return None

    async def close(self, *args, **kwargs) -> None:
        if self._conn is None:
            return
        await self._conn.close()