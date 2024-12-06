CREATE TABLE IF NOT EXISTS airlines (
    "airline_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "icao_code" CHAR(3) NOT NULL,
    "iata_code" CHAR(2) NOT NULL,
    "name" VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS destinations (
    "destination_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "longitude" FLOAT(53) NOT NULL,
    "latitude" FLOAT(53) NOT NULL
);

CREATE TABLE IF NOT EXISTS passengers (
    "passenger_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "name" VARCHAR(16) NOT NULL,
    "surname" VARCHAR(32) NOT NULL,
    "sex" VARCHAR(6) NOT NULL,
    "birth_date" DATE NOT NULL,
    "passport_number" BIGINT NOT NULL,
    "email" VARCHAR(32) NOT NULL,
    "password" VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS employees (
    "employee_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "login" VARCHAR(32) NOT NULL,
    "password" VARCHAR(64) NOT NULL,
    "name" VARCHAR(16) NOT NULL,
    "surname" VARCHAR(32) NOT NULL,
    "is_super" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS flights (
    "flight_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "airline_id" BIGINT NOT NULL REFERENCES airlines(airline_id),
    "destination_id" BIGINT NOT NULL REFERENCES destinations(destination_id),
    "number" BIGINT NOT NULL,
    "is_charter" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS departures (
    "departure_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "flight_id" BIGINT NOT NULL REFERENCES flights(flight_id),
    "status" VARCHAR(255) NOT NULL,
    "scheduled_time" TIMESTAMP(0) WITH TIME zone NOT NULL,
    "actual_time" TIMESTAMP(0) WITH TIME zone NOT NULL,
    "gate" SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS tickets (
    "ticket_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "departure_id" BIGINT NOT NULL REFERENCES departures(departure_id),
    "passenger_id" BIGINT NOT NULL REFERENCES passengers(passenger_id),
    "tariff_code" SMALLINT NOT NULL,
    "service_class" CHAR(1) NOT NULL,
    "issue_time" TIMESTAMP(0) WITH TIME zone NOT NULL,
    "is_registered" BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS boarding_pass (
    "bp_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "ticket_id" BIGINT NOT NULL REFERENCES tickets(ticket_id),
    "has_luggage" BOOLEAN NOT NULL,
    "seat" VARCHAR(3) NOT NULL,
    "issue_time" TIMESTAMP(0) WITH TIME zone NOT NULL
);

CREATE TABLE IF NOT EXISTS luggage_pass (
    "luggage_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "bp_id" BIGINT NOT NULL REFERENCES boarding_pass(bp_id),
    "weight" SMALLINT NOT NULL,
    "description" VARCHAR(100) NOT NULL
);
