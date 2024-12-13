CREATE VIEW checkin_data AS
SELECT
    tickets.ticket_id AS ticket_id,
    airlines.name AS airline_name,
    flights.number AS flight_number,
    destinations.name AS destination,
    passengers.name AS passenger_name,
    passengers.surname AS passenger_surname,
    passengers.passport_number AS passport_number
FROM
    tickets
    JOIN passengers USING(passenger_id)
    JOIN departures USING(departure_id)
    JOIN flights USING(flight_id)
    JOIN airlines USING(airline_id)
    JOIN destinations USING (destination_id);

CREATE VIEW timetable AS
SELECT
    airlines.name AS airline_name,
    airlines.iata_code AS airline_iata,
    flights.number AS flight_number,
    destinations.name AS destination,
    departures.scheduled_time AS scheduled_time,
    departures.actual_time AS actual_time
FROM
    departures
    JOIN flights USING(flight_id)
    JOIN airlines USING (airline_id)
    JOIN destinations USING (destination_id)
ORDER BY actual_time;

CREATE VIEW flights_pivot AS
SELECT
    flight_id,
    airlines.name AS airline_name,
    airlines.iata_code AS airline_iata,
    flights.number AS flight_number,
    destinations.name AS destination
FROM
    flights
    JOIN airlines USING (airline_id)
    JOIN destinations USING (destination_id);

CREATE VIEW departures_pivot AS
SELECT
    departure_id,
    airlines.name AS airline_name,
    airlines.iata_code AS airline_iata,
    flights.number AS flight_number,
    scheduled_time,
    destinations.name AS destination
FROM
    departures
    JOIN flights USING(flight_id)
    JOIN airlines USING(airline_id)
    JOIN destinations USING(destination_id); 

CREATE VIEW airlines_list AS
SELECT airline_id, name
FROM airlines;

CREATE VIEW superusers AS
SELECT employee_id
FROM employees
WHERE is_super = 'true';