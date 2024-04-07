CREATE PROCEDURE update_homonyme(IN patient_id INTEGER, IN new_first_name VARCHAR(50), IN new_last_name VARCHAR(50),
                                      IN old_first_name VARCHAR(50), IN old_last_name VARCHAR(50), IN old_homonyme INTEGER)
BEGIN
    DECLARE homonyme_count INT;

    IF new_first_name != old_first_name AND new_last_name != old_last_name THEN
        /* Calculate the new homonyme count for the updated row */
        SELECT COUNT(*) INTO homonyme_count FROM patients WHERE prenom = new_first_name AND nom = new_last_name;
        UPDATE patients SET homonyme = homonyme_count + 1 WHERE ID = patient_id;

        /* Update homonyme count for other rows with the same old_first_name and old_las_name */
        UPDATE patients
        SET homonyme = homonyme - 1
        WHERE prenom = old_first_name
        AND nom = old_last_name
        AND homonyme > old_homonyme
        AND ID != patient_id;
    END IF;
END ;