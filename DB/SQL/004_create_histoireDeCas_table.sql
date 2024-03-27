CREATE TABLE IF NOT EXISTS histoireDeCas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    conditions JSON NOT NULL,
    allergies JSON NOT NULL,
    medications JSON NOT NULL,
    trouble_vision JSON NOT NULL,
    antecedants_familiaux JSON NOT NULL,
    antecedants_oculaires JSON NOT NULL,
    examens_ID INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);