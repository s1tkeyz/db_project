from typing import Literal
from pydantic import BaseModel, Field
from datetime import date

class User(BaseModel):
    id: int = Field(..., title="User ID")
    login: str = Field(..., title="User login")
    password: str = Field(..., title="User password")
    name: str = Field(..., title="User first name", max_length=16)
    surname: str = Field(..., title="User family name", max_length=32)
    sex: Literal['male', 'female'] = Field(..., title="Sex")

class Passenger(User):
    birth_date: date = Field(..., title="Date of birth")
    passport_number: str = Field(..., title="Passport number", max_length=20)

class Employee(User):
    is_super: bool = Field(..., title="Superuser flag")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str