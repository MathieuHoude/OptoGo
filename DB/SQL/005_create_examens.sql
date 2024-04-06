CREATE TABLE IF NOT EXISTS examens (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    RX_objective JSON NOT NULL,
    RX_subjective JSON NOT NULL,
    contact_lens_type JSON NOT NULL ,
    lens_type JSON NOT NULL,
    old_RX JSON,
    periode_validite INTEGER,
    reason_next_appt varchar(50),
    patient_ID INTEGER NOT NULL,
    optometriste_ID INTEGER NOT NULL REFERENCES optometristes(ID) ON DELETE NO ACTION,
    histoireDeCas_ID INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_ID) REFERENCES patients(ID) ON DELETE NO ACTION,
    FOREIGN KEY (optometriste_ID) REFERENCES optometristes(ID) ON DELETE NO ACTION,
    FOREIGN KEY (histoireDeCas_ID) REFERENCES histoireDeCas(ID) ON DELETE NO ACTION
);