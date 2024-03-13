CREATE TABLE IF NOT EXISTS optometristes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone_number VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    exercise_number VARCHAR(10),
    address_ID INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_ID) REFERENCES addresses(ID) ON DELETE NO ACTION
);