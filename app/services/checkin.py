from random import randint, choice
from services.abstract.checkin import CheckInServiceABC
from schemas.checkin import *
from database.wrapper.postgresql import AsyncpgConnectionWrapper
from datetime import datetime, timezone
from typing import Optional, Tuple
from .cache_service import CacheService
from .notification_service import NotificationService

class CheckInService(CheckInServiceABC):
    def __init__(self):
        self.cache = CacheService()
        self.notifications = NotificationService()

    async def checkin_passenger(self, data: CheckInData) -> tuple[bool, str, tuple[int, str]]:
        query = """
        SELECT t.ticket_id, t.departure_id, t.service_class
        FROM checkin_data cd
        JOIN tickets t ON t.ticket_id = cd.ticket_id
        WHERE 
            cd.airline_name=$1 AND
            cd.flight_number=$2 AND
            cd.destination=$3 AND
            cd.passenger_name=$4 AND
            cd.passenger_surname=$5 AND
            cd.passport_number=$6
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed", (None, None))
        
        row = await conn.fetchrow(query,
                            data.airline_name,
                            data.flight_number,
                            data.destination,
                            data.passenger_name,
                            data.passenger_surname,
                            data.passport_number)
        if row is None:
            await conn.close()
            return (False, "Invalid check-in data, passenger not found", (None, None))
        
        bp = BoardingPass(
            ticket_id=row["ticket_id"],
            has_luggage=False,
            seat=f"{randint(1, 30)}{choice(['A', 'B', 'C', 'D', 'E', 'F'])}",
            issue_time=datetime.now(timezone.utc)
        )

        query = """
        INSERT INTO boarding_pass
        (ticket_id, has_luggage, seat, issue_time)
        VALUES ($1, $2, $3, $4)
        RETURNING bp_id
        """
        bp_id = await conn.fetchval(query,
                     bp.ticket_id,
                     bp.has_luggage,
                     bp.seat,
                     bp.issue_time)
        
        if bp_id:
            # Получаем информацию о регистрации для уведомления
            checkin_info = await self.get_checkin_info(row["departure_id"])
            if checkin_info:
                await self.notifications.publish_checkin_event(
                    departure_id=row["departure_id"],
                    passenger_count=checkin_info["checked_in"],
                    is_open=checkin_info["is_open"]
                )
            await conn.close()
            return (True, "OK", (bp_id, bp.seat))
        
        await conn.close()
        return (False, "Error", (None, None))

    async def get_bp(self) -> list[BoardingPass]:
        query = """
        SELECT ticket_id, has_luggage, seat, issue_time
        FROM boarding_pass
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        rows = conn.fetch(query)
        if rows is None:
            return None
        await conn.close()
        return [BoardingPass(**row) for row in rows]

    async def get_checkin_info(self, departure_id: int) -> Optional[dict]:
        """Получает информацию о регистрации на рейс"""
        # Сначала пробуем получить из кэша
        cached_info = await self.cache.get_checkin_status(departure_id)
        if cached_info:
            return cached_info

        # Если нет в кэше, получаем из БД
        query = """
        SELECT 
            d.scheduled_time,
            d.actual_time,
            COUNT(t.ticket_id) as total_tickets,
            COUNT(CASE WHEN t.is_registered THEN 1 END) as checked_in
        FROM departures d
        LEFT JOIN tickets t ON t.departure_id = d.departure_id
        WHERE d.departure_id = $1
        GROUP BY d.departure_id, d.scheduled_time, d.actual_time
        """
        
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None

        row = await conn.fetchrow(query, departure_id)
        if not row:
            return None

        # Формируем и кэшируем информацию
        info = {
            "scheduled_time": row["scheduled_time"].isoformat(),
            "actual_time": row["actual_time"].isoformat() if row["actual_time"] else None,
            "total_seats": row["total_tickets"],
            "checked_in": row["checked_in"],
            "is_open": self._is_checkin_open(row["scheduled_time"])
        }
        await self.cache.update_checkin_status(departure_id, info)
        return info

    async def register_passenger(self, ticket_id: int, departure_id: int) -> Tuple[bool, str]:
        """Регистрирует пассажира на рейс"""
        query = """
        UPDATE tickets
        SET is_registered = true
        WHERE ticket_id = $1 AND departure_id = $2
        RETURNING departure_id
        """
        
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")

        result = await conn.fetchrow(query, ticket_id, departure_id)
        await conn.close()

        if result:
            # Инвалидируем кэш для этого рейса
            await self.cache.invalidate_cache(f"checkin_status:{departure_id}")
            return (True, "Successfully registered")
        return (False, "Ticket not found or already registered")

    def _is_checkin_open(self, scheduled_time: datetime) -> bool:
        """Проверяет, открыта ли регистрация на рейс"""
        now = datetime.now(timezone.utc)
        time_before_flight = (scheduled_time - now).total_seconds() / 3600
        return 24 >= time_before_flight >= 0.5  # Регистрация открыта от 24 часов до 30 минут до вылета