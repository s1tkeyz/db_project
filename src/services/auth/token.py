import os
from typing import Tuple
from jose import jwt, JWTError
from datetime import timedelta, datetime
from ...schemas.users import *

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

class TokenService:
    @staticmethod
    async def create_access_token(user_id: int, login: str, is_employee: bool) -> Token:
        expire_date = datetime.now() + timedelta(hours=1)
        data = {
            "sub": login,
            "id": user_id,
            "is_employee": is_employee,
            "exp": expire_date
        }
        return Token(access_token=jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM), token_type="JWT")

    @staticmethod
    async def get_current_user_id(token: str) -> Tuple[int, bool] | None:
        if token is None:
            return None

        try:
            data = TokenData(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
            return data.user_id, data.is_employee
        except JWTError as e:
            return None