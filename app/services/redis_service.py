import os
import redis
from typing import Optional

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )
        self.token_expire_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", 60))

    def store_token(self, user_id: int, token: str, is_employee: bool) -> None:
        """Сохраняет токен в Redis с установленным TTL"""
        key = self._get_token_key(user_id, is_employee)
        self.redis_client.setex(
            key,
            self.token_expire_minutes * 60,  # переводим минуты в секунды
            token
        )

    def get_token(self, user_id: int, is_employee: bool) -> Optional[str]:
        """Получает токен из Redis"""
        key = self._get_token_key(user_id, is_employee)
        return self.redis_client.get(key)

    def delete_token(self, user_id: int, is_employee: bool) -> None:
        """Удаляет токен из Redis"""
        key = self._get_token_key(user_id, is_employee)
        self.redis_client.delete(key)

    def is_token_valid(self, user_id: int, token: str, is_employee: bool) -> bool:
        """Проверяет валидность токена"""
        stored_token = self.get_token(user_id, is_employee)
        return stored_token == token

    def _get_token_key(self, user_id: int, is_employee: bool) -> str:
        """Формирует ключ для токена с учетом типа пользователя"""
        user_type = "employee" if is_employee else "passenger"
        return f"token:{user_type}:{user_id}" 