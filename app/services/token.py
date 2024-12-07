import os
from datetime import timedelta, datetime
from jose import jwt, JWTError

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

class TokenService:
    async def create_token(user_id: int, login: str) -> str:
        data = {
            "sub": login,
            "id": user_id,
            "exp": datetime.now() + timedelta(hours=1)
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    async def get_user_id(token: str | None) -> int | None:
        if token is None:
            return None
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("id")
        except JWTError:
            return None