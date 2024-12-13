from pydantic import BaseModel
from typing import Literal
from datetime import date

class UserCredentials(BaseModel):
    login: str
    password: str

class User(BaseModel):
    name: str
    surname: str
    password: str

class Employee(User):
    login: str
    is_super: bool

class Passenger(User):
    sex: Literal["male", "female"]
    email: str
    passport_number: str
    birth_date: date