CREATE TRIGGER IF NOT EXISTS check_homonyme
BEFORE INSERT ON patients
FOR EACH ROW
BEGIN
    DECLARE homonyme_count INTEGER;
    SELECT COUNT(*) INTO homonyme_count FROM patients WHERE NEW.first_name = first_name AND NEW.last_name = last_name;

    SET NEW.homonyme = homonyme_count + 1;
END;
