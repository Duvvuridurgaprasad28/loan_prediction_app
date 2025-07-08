-- schema.sql

-- Create table for storing loan prediction data (only if it doesn't exist)
CREATE TABLE IF NOT EXISTS loan_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    married INTEGER,
    dependents INTEGER,
    education INTEGER,
    applicant_income FLOAT,
    coapplicant_income FLOAT,
    loan_amount FLOAT,
    loan_amount_term INTEGER,
    credit_history FLOAT,
    gender_male INTEGER,
    self_employed INTEGER,
    property_area_semiurban INTEGER,
    property_area_urban INTEGER,
    total_income FLOAT,
    prediction TEXT
);

-- Create table for storing contact data (only if it doesn't exist)
CREATE TABLE IF NOT EXISTS contact_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

