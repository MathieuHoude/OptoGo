CREATE TRIGGER IF NOT EXISTS update_histoireDeCas
BEFORE UPDATE ON histoireDeCas
FOR EACH ROW
BEGIN
    DECLARE id INTEGER;
    DECLARE patient_id INTEGER;
    DECLARE RX JSON;

    /* ONLY update periode_validite in examens if the attributes conditions -> diabetes changed 
    OR trouble_vision -> flash changed */
    IF JSON_EXTRACT(OLD.conditions, '$.diabetes') != JSON_EXTRACT(NEW.conditions, '$.diabetes') OR
       JSON_EXTRACT(OLD.trouble_vision, '$.flash') != JSON_EXTRACT(NEW.trouble_vision, '$.flash') THEN
       
       SELECT E.ID, E.patient_ID, E.RX_subjective INTO id, patient_id, RX FROM examens E WHERE E.histoireDeCas_ID = NEW.ID;

        /* +18ans */
        IF (SELECT P.birth_date FROM patients P WHERE P.ID = patient_id) < DATE_SUB(CURDATE(), INTERVAL 18 YEAR) THEN
            /* Myopie + Perception de flash */
            IF JSON_EXTRACT(RX, '$.Sphere_LE') LIKE '%-%' AND JSON_EXTRACT(NEW.trouble_vision, '$.flash') = 1 THEN
                UPDATE examens E SET E.periode_validite = 12, E.reason_next_appt = "Possible décollement de rétine" WHERE histoireDeCas_ID = NEW.ID AND E.ID = id;

            /* Diabete */
            ELSEIF JSON_EXTRACT(NEW.conditions, '$.diabetes') = 1 THEN
                UPDATE examens E SET E.periode_validite = 12, E.reason_next_appt = "Vision fluctuante à cause du diabète" WHERE histoireDeCas_ID = NEW.ID AND E.ID = id;

            ELSE
                UPDATE examens E SET E.periode_validite = 24, E.reason_next_appt = "Condition du patient normale" WHERE histoireDeCas_ID = NEW.ID AND E.ID = id;
            END IF;
        END IF;

    END IF;
END;