CREATE TABLE IF NOT EXISTS optometristes_cliniques (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    optometriste_ID INTEGER REFERENCES optometristes(ID) ON UPDATE CASCADE ON DELETE CASCADE,
    clinique_ID INTEGER REFERENCES cliniques(ID) ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (optometriste_ID) REFERENCES optometristes(ID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (clinique_ID) REFERENCES cliniques(ID) ON UPDATE CASCADE ON DELETE CASCADE
);