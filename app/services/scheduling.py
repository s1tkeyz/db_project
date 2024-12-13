from services.abstract.scheduling import SchedulingServiceABC
from schemas.scheduling import *
from database.wrapper.postgresql import AsyncpgConnectionWrapper

class SchedulingService(SchedulingServiceABC):
    async def add_airline(self, airline: Airline) -> tuple[bool, str]:
        query = """
        INSERT INTO airlines
        (name, icao_code, iata_code)
        VALUES ($1, $2, $3)
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        await conn.execute(query, airline.name, airline.icao_code, airline.iata_code)
        await conn.close()
        return (True, "OK")

    async def get_airlines(self) -> list[Airline]:
        query = """
        SELECT name, icao_code, iata_code
        FROM airlines
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query)
        return [Airline(**row) for row in rows]

    async def get_airlines_list(self) -> list[AirlineInfo] | None:
        query = """
        SELECT *
        FROM airlines_list
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query)
        return [AirlineInfo(**row) for row in rows]

    async def get_destinations_list(self) -> list[DestinationInfo] | None:
        query = """
        SELECT destination_id, name
        FROM destinations
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query)
        return [DestinationInfo(**row) for row in rows]

    async def get_flights_pivot(self) -> list[FlightInfo] | None:
        query = """
        SELECT *
        FROM flights_pivot
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query)
        return [FlightInfo(**row) for row in rows]

    async def add_destination(self, destination: Destination) -> tuple[bool, str]:
        query = """
        INSERT INTO destinations
        (name, longitude, latitude)
        VALUES ($1, $2, $3)
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        await conn.execute(query, destination.name, destination.longitude, destination.latitude)
        await conn.close()
        return (True, "OK")
    
    async def add_flight(self, flight: Flight) -> tuple[bool, str]:
        query = """
        INSERT INTO flights
        (airline_id, destination_id, number, is_charter)
        VALUES ($1, $2, $3, $4)
        RETURNING flight_id
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        id = await conn.fetchval(query, flight.airline_id, flight.destination_id, flight.number, flight.is_charter)
        await conn.close()
        if id:
            return (True, "OK")
        return (False, "Unable to add flight data")

    async def add_departure(self, departure: Departure) -> tuple[bool, str]:
        query = """
        INSERT INTO departures
        (flight_id, status, scheduled_time, actual_time, gate)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING departure_id 
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        
        id = await conn.fetchval(query,
                           departure.flight_id,
                           departure.status,
                           departure.scheduled_time,
                           departure.actual_time,
                           departure.gate
                           )
        await conn.close()
        if id:
            return (True, "OK")
        return (False, "Unable to add departure data")
    
    async def get_departures_pivot(self) -> list[DepartureInfo] | None:
        query = """
        SELECT *
        FROM departures_pivot
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query)
        return [DepartureInfo(**row) for row in rows]

    async def update_departure(self, departure_id: int, data: Departure) -> tuple[bool, str]:
        query = """
        UPDATE departures
        SET flight_id=$2, status=$3, scheduled_time=$4, actual_time=$5, gate=$6
        WHERE departure_id=$1
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return (False, "DB connection failed")
        await conn.execute(query,
                           departure_id,
                           data.flight_id,
                           data.status,
                           data.scheduled_time,
                           data.actual_time,
                           data.gate
                           )
        await conn.close()
        return (True, "OK")
        
    async def get_departures(self, skip=0, limit=10) -> list[Departure] | None:
        query = """
        SELECT flight_id, status, scheduled_time, actual_time, gate
        FROM departures
        LIMIT $1
        OFFSET $2
        """
        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        rows = await conn.fetch(query, limit, skip)
        if rows is None:
            return None
        await conn.close()
        return [Departure(**row) for row in rows]
    
    async def get_timetable(self, from_date: date, until_date: date) -> list[TimetableRow] | None:
        query = """
        SELECT *
        FROM timetable
        WHERE actual_time::DATE BETWEEN $1 AND $2
        ORDER BY actual_time
        """

        conn = AsyncpgConnectionWrapper()
        if not await conn.connect():
            return None
        
        rows = await conn.fetch(query, from_date, until_date)
        return [TimetableRow(**row) for row in rows]
