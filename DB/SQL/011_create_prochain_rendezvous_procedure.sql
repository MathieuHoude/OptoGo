CREATE PROCEDURE ajout_prochain_rendezvous()
BEGIN
    DECLARE id INTEGER;
    DECLARE d INTEGER;
    DECLARE c TIMESTAMP;

    DECLARE new_date_rendezvous TIMESTAMP;
    DECLARE existing_date_rendezvous TIMESTAMP;
    DECLARE count_date_rendezvous INTEGER;

    DECLARE lecture_complete INTEGER DEFAULT FALSE;
    DECLARE curseur CURSOR FOR SELECT E.patient_ID, E.periode_validite, E.created_at FROM examens E;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET lecture_complete = TRUE;

    OPEN curseur;
    Lecteur: LOOP
        FETCH curseur INTO id, d, c;

        IF lecture_complete THEN
            LEAVE Lecteur;
        END IF;

        SET new_date_rendezvous = DATE_ADD(c, INTERVAL d MONTH);
        SELECT MAX(R.date_rendezvous), COUNT(*) INTO existing_date_rendezvous, count_date_rendezvous FROM rendezvous R WHERE R.patients_ID = id;


        IF count_date_rendezvous > 0 THEN
            IF existing_date_rendezvous < new_date_rendezvous THEN
                UPDATE rendezvous SET date_rendezvous = new_date_rendezvous WHERE patients_ID = id;
            END IF;
        ELSEIF count_date_rendezvous = 0 THEN
            INSERT INTO rendezvous (patients_ID, date_rendezvous) VALUES (id, DATE_ADD(c, INTERVAL d MONTH));
        END IF;

    END LOOP Lecteur;
    CLOSE curseur;
END ;