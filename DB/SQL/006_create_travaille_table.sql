CREATE TABLE travaille (
    ID_optometristes SERIAL,
    ID_cliniques SERIAL,
    FOREIGN KEY (ID_optometristes) REFERENCES optometristes(ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ID_cliniques) REFERENCES cliniques(ID) ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);