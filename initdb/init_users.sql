DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'reader') THEN
        CREATE ROLE reader WITH LOGIN PASSWORD '12345678';
    END IF;
END
$$;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO reader;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO reader;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'super') THEN
        CREATE ROLE super WITH LOGIN PASSWORD '12345678' SUPERUSER;
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO super;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO super;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO super;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO super;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'reader1') THEN
        CREATE USER reader1 WITH PASSWORD '12345678';
        GRANT reader TO reader1;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'super1') THEN
        CREATE USER super1 WITH PASSWORD '12345678';
        GRANT super TO super1;
    END IF;
END
$$;