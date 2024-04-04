CREATE TRIGGER IF NOT EXISTS ajout_prochain_rendezvous
AFTER INSERT ON examens
FOR EACH ROW
BEGIN
    DECLARE new_date_rendezvous TIMESTAMP;
    DECLARE existing_date_rendezvous TIMESTAMP;
    DECLARE count_date_rendezvous INTEGER;

    SET new_date_rendezvous = DATE_ADD(NEW.created_at, INTERVAL NEW.periode_validite MONTH);
    SELECT MAX(R.date_rendezvous), COUNT(*) INTO existing_date_rendezvous, count_date_rendezvous FROM rendezvous R WHERE R.patients_ID = NEW.patient_ID;

    IF count_date_rendezvous > 0 AND existing_date_rendezvous < new_date_rendezvous THEN
            UPDATE rendezvous SET date_rendezvous = new_date_rendezvous WHERE patients_ID = NEW.patient_ID;
    ELSEIF count_date_rendezvous = 0 THEN
        INSERT INTO rendezvous (patients_ID, date_rendezvous) VALUES (NEW.patient_ID, DATE_ADD(NEW.created_at, INTERVAL NEW.periode_validite MONTH));
    END IF;

END ;