from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class User(BaseModel):
    pass

class Employee(User):
    name: str
    surname: str
    is_super: bool

class EmployeeDB(Employee):
    employee_id: int
    user_id: int

class Passenger(User):
    name: str
    surname: str
    sex: Literal["male", "female"]
    birth_date: date
    passport_number: int
    phone: str
    email: str

class PassengerDB(Passenger):
    passenger_id: int
    user_id: int