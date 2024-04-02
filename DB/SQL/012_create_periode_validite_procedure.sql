CREATE PROCEDURE ajout_periode_validite()
BEGIN
    DECLARE id INTEGER;
    DECLARE RX JSON;
    DECLARE patient_id INTEGER;
    DECLARE lecture_complete INTEGER DEFAULT FALSE;
    DECLARE curseur CURSOR FOR SELECT E.ID, E.RX_subjective, E.patient_ID FROM examens E;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET lecture_complete = TRUE;

    OPEN curseur;
    lecteur: LOOP
        FETCH curseur INTO id, RX, patient_id;

        IF lecture_complete THEN
            LEAVE lecteur;
        END IF;

        IF (SELECT E.periode_validite IS NULL FROM examens E WHERE E.ID = id) THEN

            /* POUR -18ans */
            IF (SELECT P.birth_date FROM patients P WHERE P.ID = patient_id) > DATE_SUB(CURDATE(), INTERVAL 18 YEAR) THEN
                IF CONVERT(JSON_EXTRACT(RX, '$.Sphere_LE'), SIGNED) < 0 THEN
                    UPDATE examens E SET periode_validite = 6 WHERE E.ID = id;
                ELSE
                    UPDATE examens E SET periode_validite = 12 WHERE E.ID = id;
                END IF;

            /* POUR ADULTE */
            ELSE
                /* Myopie + Perception de flash */
                IF CONVERT(JSON_EXTRACT(RX, '$.Sphere_LE'), SIGNED) < 0 AND (SELECT JSON_EXTRACT(H.trouble_vision, '$.flash') FROM histoireDeCas H INNER JOIN examens E ON H.ID = E.histoireDeCas_ID WHERE E.ID = id) = 1 THEN
                    UPDATE examens E SET periode_validite = 12 WHERE E.ID = id;

                /* Diabete */
                ELSEIF (SELECT JSON_EXTRACT(H.conditions, '$.diabetes') FROM histoireDeCas H INNER JOIN examens E ON H.ID = E.histoireDeCas_ID WHERE E.ID = id) = 1 THEN
                    UPDATE examens E SET periode_validite = 12 WHERE E.ID = id;

                ELSE
                    UPDATE examens E SET periode_validite = 24 WHERE E.ID = id;
                END IF;
            END IF;
        END IF;

    END LOOP lecteur;
    CLOSE curseur;
    CALL ajout_prochain_rendezvous();

END ;