from ..abstract.user import UserServiceABC
from typing import Tuple
from ...schemas.user import *
from ...database.handlers.postgresql import PosgreSQLConnectionWrapper
from passlib.context import CryptContext

class PassengerService(UserServiceABC):
    def __init__(self):
        self._crypt_ctx = CryptContext(schemes=["sha256_crypt"])

    async def authentificate_user(self, credentials: UserCredentials) -> int | None:
        conn = PosgreSQLConnectionWrapper()
        query = """
        SELECT passenger_id, password
        FROM passengers
        WHERE email = $1
        """
        try:
            await conn.connect()
            row = await conn.fetchrow(query, credentials.login)
            conn.close()
            if row is None:
                return None
            if self._crypt_ctx.verify(credentials.password, row["password"]):
                return row["passenger_id"]
            return None
        finally:
            return None
    
    async def add_user(self, passenger: Passenger) -> Tuple[bool, str]:
        conn = PosgreSQLConnectionWrapper()
        try:
            await conn.connect()
            query = """
            SELECT passenger_id
            FROM passengers
            WHERE email = $1
            """
            data = await conn.fetchrow(query, passenger.email)
            if data is not None:
                return False, "Passenger with this E-Mail already exists"
            query = """
            INSERT INTO passengers
            (name, surname, sex, birth_date, passport_number, email, password)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """
            await conn.execute(query, **passenger.model_dump())
            await conn.close()
            return True, "OK"
        finally:
            return False, "Query error"
    
    async def get_user_info(self, passenger_id: int) -> Passenger | None:
        query = """
        SELECT name, surname, sex, birth_date, passport_number, email, password
        FROM passengers
        WHERE passenger_id = $1
        """
        conn = PosgreSQLConnectionWrapper()
        try:
            await conn.connect()
            row = await conn.fetchrow(query, passenger_id)
            conn.close()
            if row is None:
                return None
            return Passenger(**row)
        finally:
            return None
