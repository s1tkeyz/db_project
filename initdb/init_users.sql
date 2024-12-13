CREATE USER readonly_user WITH PASSWORD '12345678';

GRANT CONNECT ON DATABASE airport TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;

--GRANT SELECT ON airlines TO readonly_user;
--GRANT SELECT ON destinations TO readonly_user;
--GRANT SELECT ON flights TO readonly_user;
--GRANT SELECT ON departures TO readonly_user;
--GRANT SELECT ON tickets TO readonly_user;
--GRANT SELECT ON passengers TO readonly_user;
--GRANT SELECT ON employees TO readonly_user;
--GRANT SELECT ON boarding_pass TO readonly_user;

--GRANT SELECT ON checkin_data TO readonly_user;
--GRANT SELECT ON timetable TO readonly_user;
--GRANT SELECT ON flights_pivot TO readonly_user;
--GRANT SELECT ON airlines_list TO readonly_user;
--GRANT SELECT ON superusers TO readonly_user;
--GRANT SELECT ON departures_pivot TO readonly_user;