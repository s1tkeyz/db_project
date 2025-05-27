import os
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from .redis_service import RedisService

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

class TokenService:
    def __init__(self):
        self.redis_service = RedisService()

    async def create_token(self, user_id: int, login: str, is_employee: bool = False) -> str:
        data = {
            "sub": login,
            "id": user_id,
            "emp": is_employee,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("TOKEN_EXPIRE_MINUTES", 60)))
        }
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        self.redis_service.store_token(user_id, token, is_employee)
        return token

    async def get_user_info(self, token: str | None) -> tuple[int, bool] | None:
        if token is None:
            return (None, None)
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = decoded.get("id")
            is_employee = decoded.get("emp", False)
            
            # Проверяем, что токен действителен и хранится в Redis
            if not self.redis_service.is_token_valid(user_id, token, is_employee):
                return (None, None)
                
            return (user_id, is_employee)
        except JWTError:
            return (None, None)

    async def invalidate_token(self, user_id: int, is_employee: bool = False) -> None:
        """Инвалидирует токен пользователя"""
        self.redis_service.delete_token(user_id, is_employee)
