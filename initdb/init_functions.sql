CREATE OR REPLACE FUNCTION log_checkin()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO checkin_logs (ticket_id)
    VALUES (NEW.ticket_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER checkin_logger
AFTER INSERT ON boarding_pass
FOR EACH ROW EXECUTE FUNCTION log_checkin();

CREATE OR REPLACE FUNCTION erase_registered_tickets()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM tickets
    WHERE is_registered = 'true';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ticket_trunc
AFTER UPDATE ON tickets
FOR EACH ROW EXECUTE FUNCTION erase_registered_tickets();