import json
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from .redis_service import RedisService

class NotificationService:
    CHANNELS = {
        'flight_status': 'notifications:flight_status',
        'checkin': 'notifications:checkin',
        'booking': 'notifications:booking',
        'gate_changes': 'notifications:gate_changes'
    }

    def __init__(self):
        self.redis = RedisService()
        self.pubsub = self.redis.redis_client.pubsub()

    async def publish_flight_status_change(self, departure_id: int, status: str, 
                                         scheduled_time: datetime, actual_time: Optional[datetime] = None) -> None:
        """Публикует уведомление об изменении статуса рейса"""
        message = {
            'event_type': 'flight_status_change',
            'departure_id': departure_id,
            'new_status': status,
            'scheduled_time': scheduled_time.isoformat(),
            'actual_time': actual_time.isoformat() if actual_time else None,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self._publish(self.CHANNELS['flight_status'], message)

    async def publish_checkin_event(self, departure_id: int, passenger_count: int, 
                                  is_open: bool) -> None:
        """Публикует уведомление о событии регистрации"""
        message = {
            'event_type': 'checkin_update',
            'departure_id': departure_id,
            'passenger_count': passenger_count,
            'is_open': is_open,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self._publish(self.CHANNELS['checkin'], message)

    async def publish_booking_event(self, departure_id: int, ticket_id: int, 
                                  service_class: str) -> None:
        """Публикует уведомление о новом бронировании"""
        message = {
            'event_type': 'new_booking',
            'departure_id': departure_id,
            'ticket_id': ticket_id,
            'service_class': service_class,
            'timestamp': datetime.utcnow().isoformat()
        }
        await self._publish(self.CHANNELS['booking'], message)

    async def publish_gate_change(self, departure_id: int, new_gate: int, 
                                scheduled_time: datetime) -> None:
        """Публикует уведомление об изменении гейта"""
        message = {
            'event_type': 'gate_change',
            'departure_id': departure_id,
            'new_gate': new_gate,
            'scheduled_time': scheduled_time.isoformat(),
            'timestamp': datetime.utcnow().isoformat()
        }
        await self._publish(self.CHANNELS['gate_changes'], message)

    async def _publish(self, channel: str, message: Dict[str, Any]) -> None:
        """Публикует сообщение в канал"""
        self.redis.redis_client.publish(channel, json.dumps(message))

    async def subscribe(self, channels: list[str], callback: Callable[[str, Dict[str, Any]], None]) -> None:
        """Подписывается на каналы и обрабатывает сообщения через callback"""
        self.pubsub.subscribe(*channels)
        
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                channel = message['channel'].decode('utf-8')
                data = json.loads(message['data'].decode('utf-8'))
                callback(channel, data)

    def close(self) -> None:
        """Закрывает подключение"""
        self.pubsub.close() 