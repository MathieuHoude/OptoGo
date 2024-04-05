CREATE PROCEDURE IF NOT EXISTS liste_patients_du()
BEGIN
    SELECT DISTINCT P.*
    FROM patients P
    INNER JOIN rendezvous R ON P.ID = R.patients_ID
    WHERE DATE(R.date_rendezvous) < CURDATE();
END;
