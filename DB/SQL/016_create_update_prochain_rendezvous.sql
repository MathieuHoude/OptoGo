CREATE TRIGGER IF NOT EXISTS update_prochain_rendezvous
BEFORE UPDATE ON examens
FOR EACH ROW
BEGIN
    /* Update date in table rendezvous only if periode_validite is different */
    IF OLD.periode_validite != NEW.periode_validite THEN
        UPDATE rendezvous SET date_rendezvous = DATE_ADD(NEW.created_at, INTERVAL NEW.periode_validite MONTH) WHERE patients_ID = NEW.patient_ID;

    /* Update periode_validite if RX_subjectve changed */
    ELSEIF OLD.RX_subjective != NEW.RX_subjective THEN
        IF (SELECT P.birth_date FROM patients P WHERE P.ID = NEW.patient_ID) > DATE_SUB(CURDATE(), INTERVAL 18 YEAR) THEN
            /* Myopie */
            IF JSON_EXTRACT(NEW.RX_subjective, '$.Sphere_LE') LIKE '%-%' THEN
                SET NEW.periode_validite = 6;
                UPDATE rendezvous SET date_rendezvous = DATE_ADD(NEW.created_at, INTERVAL NEW.periode_validite MONTH) WHERE patients_ID = NEW.patient_ID;
            END IF;
        ELSE
            /* Myopie + Perception de flash */
            IF JSON_EXTRACT(NEW.RX_subjective, '$.Sphere_LE') LIKE '%-%' AND (SELECT JSON_EXTRACT(H.trouble_vision, '$.flash') FROM histoireDeCas H WHERE H.ID = NEW.histoireDeCas_ID) = 1 THEN
                SET NEW.periode_validite = 12;
                UPDATE rendezvous SET date_rendezvous = DATE_ADD(NEW.created_at, INTERVAL NEW.periode_validite MONTH) WHERE patients_ID = NEW.patient_ID;
            END IF;
        END IF;
    END IF;
END ;