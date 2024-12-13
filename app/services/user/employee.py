from services.abstract.user import UserServiceABC
from schemas.user import *
from database.wrapper.postgresql import AsyncpgConnectionWrapper
from passlib.context import CryptContext

class EmployeeService(UserServiceABC):
    def __init__(self):
        self._hasher = CryptContext(schemes=["sha256_crypt"])

    async def auth_user(self, credentials: UserCredentials) -> int | None:
        query = """
        SELECT employee_id, password
        FROM employees
        WHERE login = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        row = await conn.fetchrow(query, credentials.login)
        await conn.close()
        if (row is None) or (not self._hasher.verify(credentials.password, row["password"])):
            return None
        return row["employee_id"]  

    async def add_user(self, employee: Employee) -> tuple[bool, str]:
        query = """
        INSERT INTO employees
        (login, password, name, surname, is_super)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING employee_id 
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        employee.password = self._hasher.hash(employee.password)
        id = await conn.fetchval(query,
                           employee.login,
                           employee.password,
                           employee.name,
                           employee.surname,
                           employee.is_super)
        await conn.close()
        if id:
            return (True, "OK")
        return (False, "Employee with this login already exists")
        
    async def remove_user(self, employee_id: int) -> tuple[bool, str]:
        ...

    async def get_user_info(self, employee_id: int) -> Employee:
        query = """
        SELECT login, password, name, surname, is_super
        FROM employees
        WHERE employee_id = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        row = await conn.fetchrow(query, employee_id)
        await conn.close()
        return Employee(**row)
    
    async def edit_user(self, employee_id: int, employee: Employee) -> tuple[bool, str]:
        employee.password = self._hasher.hash(employee.password)
        query = """
        UPDATE employees
        SET login=$2, password=$3, name=$4, surname=$5, is_super=$6
        WHERE employee_id = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")

        await conn.execute(query,
                           employee_id,
                           employee.login,
                           employee.password,
                           employee.name,
                           employee.surname,
                           employee.is_super
                           )
        await conn.close()
        return (True, "OK")
    
    async def is_super(self, employee_id: int) -> bool | None:
        query = """
        SELECT *
        FROM superusers
        WHERE employee_id = $1
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        
        row = await conn.fetchrow(query, employee_id)
        await conn.close()
        if row is None:
            return None
        return True

    async def get_users(self) -> list[Employee]:
        query = """
        SELECT login, password, name, surname, is_super
        FROM employees
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return []

        employees = []
        rows = await conn.fetch(query)
        for row in rows:
            employees.append(Employee(**row))
        return employees
