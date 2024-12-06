from pydantic import BaseModel, Field
from typing import Literal
from datetime import date, datetime
from enum import Enum

class UserRole(Enum):
    UNKNOWN = 0
    PASSENGER = 1
    EMPLOYEE = 2
    SUPERUSER = 3

class User(BaseModel):
    user_id: int = Field(..., title="User ID", ge=0)
    login: str = Field(..., title="User login", max_length=32)
    password: str = Field(..., title="User password", max_length=64)
    is_employee: bool = Field(..., title="Is employee?")

class UserCredentials(BaseModel):
    login: str
    password: str