from typing import Literal
from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum

class UserRole(Enum):
    PASSENGER = 0
    CHECKIN = 1
    SUPERUSER = 2

class UserCredentials(BaseModel):
    """
    User auth credentials model
    """
    login: str
    password: str
    is_employee: bool

class User(BaseModel):
    """
    General user data model
    """
    name: str = Field(..., title="User first name", max_length=16)
    surname: str = Field(..., title="User family name", max_length=32)
    password: str = Field(..., title="User password")
    sex: Literal["male", "female"] = Field(..., title="Sex")

class UserDB(User):
    """
    General user database representation model
    """
    user_id: int = Field(..., title="User ID", ge=0)

class Passenger(User):
    """
    Passenger data model
    """
    birth_date: date = Field(..., title="Date of birth")
    passport_number: str = Field(..., title="Passport number", max_length=20)
    phone: str = Field(..., title="Passenger's phone number", max_length=16)
    email: str = Field(..., title="Passenger's E-Mail adress", max_length=32)

class PassengerDB(UserDB, Passenger):
    """
    Passenger database representation model
    """
    pass

class Employee(User):
    """
    Employee data model
    """
    login: str = Field(..., title="Employee's system login", max_length=16)
    is_super: bool = Field(..., title="Superuser flag")

class EmployeeDB(UserDB, Employee):
    """
    Employee database representation model
    """
    pass

class Token(BaseModel):
    """
    Auth token model
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Auth token data model
    """
    user_id: int
    login: str
    is_employee: bool
    expires: datetime