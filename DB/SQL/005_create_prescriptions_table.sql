CREATE TABLE IF NOT EXISTS prescriptions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    periode_validite INTEGER NOT NULL,
    optometriste VARCHAR(50) NOT NULL,
    date_prescriptions DATE NOT NULL,
    puissance JSON NOT NULL,
    examens_ID INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);