import os
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

class TokenService:
    async def create_token(self, user_id: int, login: str, is_employee: bool = False) -> str:
        data = {
            "sub": login,
            "id": user_id,
            "emp": is_employee,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    async def get_user_info(self, token: str | None) -> tuple[int, bool] | None:
        if token is None:
            return (None, None)
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return (decoded.get("id"), decoded.get("emp"))
        except JWTError:
            return (None, None)
