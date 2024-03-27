CREATE TABLE IF NOT EXISTS examens (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    RX_objective JSON NOT NULL,
    RX_subjective JSON NOT NULL,
    adjustment JSON NOT NULL, --Port de verre de contact
    lens_type JSON NOT NULL, --Type de lunette porté
    old_RX JSON NOT NULL,
    patient_ID INTEGER NOT NULL,
    optometriste_ID INTEGER NOT NULL REFERENCES optometristes(ID) ON DELETE NO ACTION,
    histoireDeCas_ID INTEGER NOT NULL,
    prescriptions_ID INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_ID) REFERENCES patients(ID) ON DELETE NO ACTION,
    FOREIGN KEY (optometriste_ID) REFERENCES optometristes(ID) ON DELETE NO ACTION,
    FOREIGN KEY (histoireDeCas_ID) REFERENCES histoireDeCas(ID) ON DELETE NO ACTION,
    FOREIGN KEY (prescriptions_ID) REFERENCES prescriptions(ID) ON DELETE NO ACTION
);