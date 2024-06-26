CREATE TABLE IF NOT EXISTS rendezvous (
    patients_ID INTEGER PRIMARY KEY,
    date_rendezvous TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(patients_ID) REFERENCES patients(ID) ON UPDATE CASCADE ON DELETE CASCADE
);