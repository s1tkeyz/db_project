import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from .redis_service import RedisService

class CacheService:
    def __init__(self):
        self.redis = RedisService()

    def _serialize_datetime(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Преобразует datetime объекты в ISO формат для JSON сериализации"""
        result = {}
        for key, value in obj.items():
            if isinstance(value, datetime):
                # Убеждаемся, что datetime имеет временную зону
                if value.tzinfo is None:
                    value = value.replace(tzinfo=timezone.utc)
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    async def cache_flight_status(self, departure_id: int, status: dict) -> None:
        """Кэширует статус рейса"""
        key = f"flight_status:{departure_id}"
        status["last_updated"] = datetime.now(timezone.utc).isoformat()
        self.redis.redis_client.setex(
            key,
            24 * 60 * 60,  # 24 часа
            json.dumps(self._serialize_datetime(status))
        )

    async def get_flight_status(self, departure_id: int) -> Optional[dict]:
        """Получает статус рейса из кэша"""
        key = f"flight_status:{departure_id}"
        data = self.redis.redis_client.get(key)
        return json.loads(data) if data else None

    async def cache_schedule(self, date: str, schedule: List[Dict[str, Any]]) -> None:
        """Кэширует расписание на определенную дату"""
        key = f"schedule:{date}"
        serialized_schedule = [self._serialize_datetime(item) for item in schedule]
        self.redis.redis_client.setex(
            key,
            60 * 60,  # 1 час
            json.dumps(serialized_schedule)
        )

    async def get_schedule(self, date: str) -> Optional[List[Dict[str, Any]]]:
        """Получает расписание из кэша"""
        key = f"schedule:{date}"
        data = self.redis.redis_client.get(key)
        return json.loads(data) if data else None

    async def update_checkin_status(self, departure_id: int, status: dict) -> None:
        """Обновляет статус регистрации на рейс"""
        key = f"checkin_status:{departure_id}"
        self.redis.redis_client.set(key, json.dumps(self._serialize_datetime(status)))
        # TTL установим до времени вылета
        if "scheduled_time" in status:
            scheduled_time = datetime.fromisoformat(status["scheduled_time"])
            # Убеждаемся, что обе даты имеют временную зону UTC
            if scheduled_time.tzinfo is None:
                scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
            current_time = datetime.now(timezone.utc)
            ttl = int((scheduled_time - current_time).total_seconds())
            if ttl > 0:
                self.redis.redis_client.expire(key, ttl)

    async def get_checkin_status(self, departure_id: int) -> Optional[dict]:
        """Получает статус регистрации на рейс"""
        key = f"checkin_status:{departure_id}"
        data = self.redis.redis_client.get(key)
        return json.loads(data) if data else None

    async def update_user_session(self, user_id: int, session_data: dict) -> None:
        """Обновляет данные сессии пользователя"""
        key = f"session:{user_id}"
        session_data["last_activity"] = datetime.now(timezone.utc).isoformat()
        self.redis.redis_client.setex(
            key,
            30 * 60,  # 30 минут
            json.dumps(self._serialize_datetime(session_data))
        )

    async def get_user_session(self, user_id: int) -> Optional[dict]:
        """Получает данные сессии пользователя"""
        key = f"session:{user_id}"
        data = self.redis.redis_client.get(key)
        return json.loads(data) if data else None

    async def invalidate_cache(self, pattern: str) -> None:
        """Инвалидирует кэш по паттерну"""
        for key in self.redis.redis_client.scan_iter(pattern):
            self.redis.redis_client.delete(key) 