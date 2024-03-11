CREATE TABLE examens (
    ID SERIAL PRIMARY KEY,
    RX_objective VARCHAR(50) NOT NULL,
    RX_subjective VARCHAR(50) NOT NULL,
    acuite INTEGER NOT NULL,
    adjustment VARCHAR(50) NOT NULL,
    lens_type VARCHAR(50) NOT NULL,
    effectue INTEGER NOT NULL, --participation unaire avec patients
    realise INTEGER NOT NULL, --participation unaire avec optometristes
    FOREIGN KEY (effectue) REFERENCES patients(ID) ON DELETE NO ACTION,
    FOREIGN KEY (realise) REFERENCES optometristes(ID) ON DELETE NO ACTION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);