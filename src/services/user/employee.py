from ..abstract.user import UserServiceABC
from typing import Tuple
from ...schemas.user import *
from ...database.handlers.postgresql import PosgreSQLConnectionWrapper
from passlib.context import CryptContext

class EmployeeService(UserServiceABC):
    def __init__(self):
        self._crypt_ctx = CryptContext(schemes=["sha256_crypt"])

    async def authentificate_user(self, credentials: UserCredentials) -> int | None:
        conn = PosgreSQLConnectionWrapper()
        query = """
        SELECT employee_id, password
        FROM employees
        WHERE login = $1
        """
        try:
            await conn.connect()
            row = await conn.fetchrow(query, credentials.login)
            conn.close()
            if row is None:
                return None
            if self._crypt_ctx.verify(credentials.password, row["password"]):
                return row["employee_id"]
            return None
        finally:
            return None
    
    async def add_user(self, employee: Employee) -> Tuple[bool, str]:
        conn = PosgreSQLConnectionWrapper()
        try:
            await conn.connect()
            query = """
            SELECT employee_id
            FROM employees
            WHERE login = $1
            """
            data = await conn.fetchrow(query, employee.login)
            if data is not None:
                return False, "Employee with this login already exists"
            query = """
            INSERT INTO employees
            (login, password, name, surname, is_super)
            VALUES ($1, $2, $3, $4, $5)
            """
            await conn.execute(query, **employee.model_dump())
            await conn.close()
            return True, "OK"
        finally:
            return False, "Query error"
    
    async def get_user_info(self, employee_id: int) -> Employee | None:
        query = """
        SELECT login, password, name, surname, is_super
        FROM employees
        WHERE employee_id = $1
        """
        conn = PosgreSQLConnectionWrapper()
        try:
            await conn.connect()
            row = await conn.fetchrow(query, employee_id)
            conn.close()
            if row is None:
                return None
            return Employee(**row)
        finally:
            return None
