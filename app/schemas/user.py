from pydantic import BaseModel
from typing import Literal
from datetime import date, datetime

class User(BaseModel):
    name: str
    surname: str
    password: str

class UserCredentials(BaseModel):
    login: str
    password: str

class Passenger(User):
    sex: Literal["male", "female"]
    birth_date: datetime
    passport_number: int
    email: str

class Employee(User):
    login: str
    is_super: bool