import os
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from ..abc import user
from ...schemas.users import *
from typing import Tuple
from ...database.handlers.postgresql import PosgreSQLConnectionWrapper

class PassengerUserService(user.UserServiceABC):
    def __init__(self) -> None:
        self._crypt_ctx = CryptContext(schemes=["bcrypt"])

    async def authentificate_user(self, passenger_email: str, passenger_password: str) -> int | None:
        query = """
        SELECT passenger_id
        FROM passengers 
        WHERE email = $1 AND password = $2
        """
        conn = PosgreSQLConnectionWrapper()
        conn.connect()
        try:
            passenger = PassengerDB(**conn.fetchrow(query, passenger_email, passenger_password))
            return passenger.user_id
        finally:
            return None

    async def add_new_user(self, passenger_data: Passenger) -> Tuple[bool, str]:
        ...
    
    async def remove_user(self, passenger_id: int) -> Tuple[bool, str]:
        ...

    async def get_user_info(self, passenger_id: int) -> Passenger | None:
        query = """
        SELECT *
        FROM passengers 
        WHERE passenger_id = $1
        """
        conn = PosgreSQLConnectionWrapper()
        conn.connect()
        try:
            data = conn.fetchrow(query, passenger_id)
            return Passenger(*[v for f, v in data.items()])
        finally:
            return None

    async def update_user(self, passenger_id: int, passenger_data: Passenger) -> Tuple[bool, str]:
        ...