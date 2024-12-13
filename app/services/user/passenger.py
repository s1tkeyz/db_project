from services.abstract.user import UserServiceABC
from schemas.user import *
from database.wrapper.postgresql import AsyncpgConnectionWrapper
from passlib.context import CryptContext

class PassengerService(UserServiceABC):
    def __init__(self):
        self._hasher = CryptContext(schemes=["sha256_crypt"])

    async def auth_user(self, credentials: UserCredentials) -> int | None:
        query = """
        SELECT passenger_id, password
        FROM passengers
        WHERE email = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        row = await conn.fetchrow(query, credentials.login)
        await conn.close()
        if (row is None) or (not self._hasher.verify(credentials.password, row["password"])):
            return None
        return row["passenger_id"]  

    async def add_user(self, passenger: Passenger) -> tuple[bool, str]:
        query = """
        INSERT INTO passengers
        (name, surname, sex, birth_date, passport_number, email, password)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING passenger_id
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        passenger.password = self._hasher.hash(passenger.password)
        id = await conn.fetchval(query,
                           passenger.name,
                           passenger.surname,
                           passenger.sex,
                           passenger.birth_date,
                           passenger.passport_number,
                           passenger.email,
                           passenger.password
                           )
        await conn.close()
        if id is not None:
            return (True, "OK")
        return (False, "Invalid data")
        
    async def remove_user(self, passenger_id: int) -> tuple[bool, str]:
        ...

    async def get_user_info(self, passenger_id: int) -> Passenger:
        query = """
        SELECT name, surname, sex, birth_date, passport_number, email, password
        FROM passengers
        WHERE passenger_id = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        row = await conn.fetchrow(query, passenger_id)
        await conn.close()
        return Passenger(**row)
    
    async def edit_user(self, passenger_id: int, passenger: Passenger) -> tuple[bool, str]:
        passenger.password = self._hasher.hash(passenger.password)
        query = """
        UPDATE passengers
        SET name=$2, surname=$3, sex=$4, birth_date=$5, passport_number=$6, email=$7, password=$8
        WHERE passenger_id = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")

        await conn.execute(query,
                           passenger_id,
                           passenger.name,
                           passenger.surname,
                           passenger.sex,
                           passenger.birth_date,
                           passenger.passport_number,
                           passenger.email,
                           passenger.password
                           )
        await conn.close()
        return (True, "OK")

    async def get_users(self) -> list[Passenger]:
        query = """
        SELECT name, surname, sex, birth_date, passport_number, email, password
        FROM passengers
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return []

        passengers = []
        rows = await conn.fetch(query)
        for row in rows:
            passengers.append(Passenger(**row))
        return passengers