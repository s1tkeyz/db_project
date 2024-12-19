from random import randint, choice
from services.abstract.checkin import CheckInServiceABC
from schemas.checkin import *
from database.wrapper.postgresql import AsyncpgConnectionWrapper
from datetime import datetime, timezone

class CheckInService(CheckInServiceABC):
    async def checkin_passenger(self, data: CheckInData) -> tuple[bool, str, tuple[int, str]]:
        query = """
        SELECT *
        FROM checkin_data
        WHERE 
            airline_name=$1 AND
            flight_number=$2 AND
            destination=$3 AND
            passenger_name=$4 AND
            passenger_surname=$5 AND
            passport_number=$6
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
        await conn.close()
        if bp_id:
            return (True, "OK", (bp_id, bp.seat))
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