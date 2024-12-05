import os
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import timedelta, datetime
from ..abc import user
from ...schemas.users import *
from typing import Tuple
from ...database.handlers.postgresql import PosgreSQLConnectionWrapper

class EmployeeUserService(user.UserServiceABC):
    def __init__(self) -> None:
        self._crypt_ctx = CryptContext(schemes=["bcrypt"])
    
    async def authentificate_user(self, employee_login: str, employee_password: str) -> int | None:
        query = """
        SELECT employee_id
        FROM employees 
        WHERE login = $1 AND password = $2
        """
        conn = PosgreSQLConnectionWrapper()
        conn.connect()
        try:
            employee = EmployeeDB(**conn.fetchrow(query, employee_login, employee_password))
            
            return employee.user_id
        finally:
            return None

    async def add_new_user(self, employee_data: Employee) -> Tuple[bool, str]:
        ...
    
    async def remove_user(self, employee_id: int) -> Tuple[bool, str]:
        ...

    async def get_user_info(self, employee_id: int) -> Employee | None:
        query = """
        SELECT *
        FROM employees 
        WHERE employee_id = $1
        """
        conn = PosgreSQLConnectionWrapper()
        conn.connect()
        try:
            data = conn.fetchrow(query, employee_id)
            return Employee(*[v for f, v in data.items()])
        finally:
            return None

    async def update_user(self, employee_id: int, employee_data: Employee) -> Tuple[bool, str]:
        ...
