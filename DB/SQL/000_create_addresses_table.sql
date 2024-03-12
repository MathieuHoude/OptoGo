CREATE TABLE IF NOT EXISTS addresses (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    street_number VARCHAR(10) NOT NULL,
    street_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    province VARCHAR(20) NOT NULL,
    postal_code CHAR(6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);