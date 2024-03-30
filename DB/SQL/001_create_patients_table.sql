CREATE TABLE IF NOT EXISTS patients (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    RAMQ_number VARCHAR(20) UNIQUE,
    homonyme INTEGER NOT NULL,
    address_ID INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_ID) REFERENCES addresses(ID) ON DELETE NO ACTION
);