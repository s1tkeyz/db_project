from schemas.ticket import *
from services.abstract.ticket import TicketServiceABC
from datetime import datetime, timezone
from database.wrapper.postgresql import AsyncpgConnectionWrapper
from .notification_service import NotificationService

class TicketService(TicketServiceABC):
    def __init__(self):
        self.notifications = NotificationService()

    async def book_ticket(self, data: BookingData) -> tuple[bool, str]:
        query = """
        INSERT INTO tickets
        (departure_id, passenger_id, tariff_code, service_class, issue_time, is_registered)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING ticket_id
        """
        
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        ticket_id = await conn.fetchval(query,
                           data.departure_id,
                           data.passenger_id,
                           data.tariff_code,
                           data.service_class,
                           datetime.now(timezone.utc),
                           False
                           )
        await conn.close()

        if ticket_id:
            # Отправляем уведомление о новом бронировании
            await self.notifications.publish_booking_event(
                departure_id=data.departure_id,
                ticket_id=ticket_id,
                service_class=data.service_class
            )
            return (True, "OK")
        return (False, "Unable to book ticket")

    async def get_tickets(self) -> list[Ticket]:
        query = """
        SELECT departure_id, passenger_id, tariff_code, is_registered, service_class
        FROM tickets
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        rows = conn.fetch(query)
        if rows is None:
            return None
        await conn.close()
        return [Ticket(**row) for row in rows]