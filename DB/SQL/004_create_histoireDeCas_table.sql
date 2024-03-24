CREATE TABLE IF NOT EXISTS histoireDeCas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    conditions VARCHAR(50) NOT NULL,
    allergies VARCHAR(50) NOT NULL,
    medications VARCHAR(50) NOT NULL,
    trouble_vision VARCHAR(50) NOT NULL,
    antecedants_familiaux VARCHAR(50) NOT NULL,
    antecedants_oculaires VARCHAR(50) NOT NULL,
    examens_ID INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);