CREATE FUNCTION IF NOT EXISTS nombre_patients_du() RETURNS INTEGER DETERMINISTIC
BEGIN
    DECLARE nombre INTEGER;
    SELECT COUNT(*) INTO nombre FROM rendezvous WHERE DATE(date_rendezvous) < CURDATE();

    return nombre;
END ;