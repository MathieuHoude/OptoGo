CREATE TRIGGER IF NOT EXISTS ajout_periode_validite
BEFORE INSERT ON examens
FOR EACH ROW
BEGIN

    /* POUR -18ans */
    IF (SELECT P.birth_date FROM patients P WHERE P.ID = NEW.patient_ID) > DATE_SUB(CURDATE(), INTERVAL 18 YEAR) THEN
        /* Myopie */
        IF JSON_EXTRACT(NEW.RX_subjective, '$.Sphere_LE') LIKE '%-%' THEN
            SET NEW.periode_validite = 6;
            SET NEW.reason_next_appt = "Possible évolution myopique";
        ELSE
            SET NEW.periode_validite = 12;
            SET NEW.reason_next_appt = "Enfant";
        END IF;

    /* POUR ADULTE */
    ELSE
        /* Myopie + Perception de flash */
        IF JSON_EXTRACT(NEW.RX_subjective, '$.Sphere_LE') LIKE '%-%' AND (SELECT JSON_EXTRACT(H.trouble_vision, '$.flash') FROM histoireDeCas H WHERE H.ID = NEW.histoireDeCas_ID) = 1 THEN
            SET NEW.periode_validite = 12;
            SET NEW.reason_next_appt = "Possible décollement de rétine";

        /* Diabete */
        ELSEIF (SELECT JSON_EXTRACT(H.conditions, '$.diabetes') FROM histoireDeCas H WHERE H.ID = NEW.histoireDeCas_ID) = 1 THEN
            SET NEW.periode_validite = 12;
            SET NEW.reason_next_appt = "Vision fluctuante à cause du diabète";

        ELSE
            SET NEW.periode_validite = 24;
            SET NEW.reason_next_appt = "Condition du patient normale";
        END IF;
    END IF;
END;