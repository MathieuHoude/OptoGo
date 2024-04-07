CREATE TRIGGER IF NOT EXISTS update_histoireDeCas
BEFORE UPDATE ON histoireDeCas
FOR EACH ROW
BEGIN
    IF JSON_EXTRACT(OLD.conditions, '$.diabetes') != JSON_EXTRACT(NEW.conditions, '$.diabetes') OR
       JSON_EXTRACT(OLD.trouble_vision, '$.flash') != JSON_EXTRACT(NEW.trouble_vision, '$.flash') THEN

        CALL process_rows_examens(NEW.ID, NEW.conditions, NEW.trouble_vision);

    END IF;
END;