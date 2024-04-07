CREATE PROCEDURE process_rows_examens(IN NEW_id INTEGER, IN NEW_conditions JSON, IN NEW_trouble_vision JSON)
BEGIN
    DECLARE id INTEGER;
    DECLARE patient_id INTEGER;
    DECLARE RX JSON;

    DECLARE lecture_complete INTEGER DEFAULT FALSE;
    DECLARE curseur CURSOR FOR SELECT E.ID, E.patient_ID, E.RX_subjective FROM examens E WHERE E.histoireDeCas_ID = NEW_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET lecture_complete = TRUE;

    OPEN curseur;
    lecteur:LOOP
        FETCH curseur INTO id, patient_id, RX;
        IF lecture_complete THEN
            LEAVE lecteur;
        END IF;

        /* +18ans */
        IF (SELECT P.birth_date FROM patients P WHERE P.ID = patient_id) < DATE_SUB(CURDATE(), INTERVAL 18 YEAR) THEN
            /* Myopie + Perception de flash */
            IF JSON_EXTRACT(RX, '$.Sphere_LE') LIKE '%-%' AND JSON_EXTRACT(NEW_trouble_vision, '$.flash') = 1 THEN
                UPDATE examens E SET E.periode_validite = 12, E.reason_next_appt = "Possible décollement de rétine" WHERE histoireDeCas_ID = NEW_id AND E.ID = id;

            /* Diabete */
            ELSEIF JSON_EXTRACT(NEW_conditions, '$.diabetes') = 1 THEN
                UPDATE examens E SET E.periode_validite = 12, E.reason_next_appt = "Vision fluctuante à cause du diabète" WHERE histoireDeCas_ID = NEW_id AND E.ID = id;

            ELSE
                UPDATE examens E SET E.periode_validite = 24, E.reason_next_appt = "Condition du patient normale" WHERE histoireDeCas_ID = NEW_id AND E.ID = id;
            END IF;
        END IF;

    END LOOP lecteur;
    CLOSE curseur;
END ;