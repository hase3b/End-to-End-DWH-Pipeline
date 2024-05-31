-- Database: Real-Estate-Management

-- DROP DATABASE IF EXISTS "Real-Estate-Management";

CREATE DATABASE "Real-Estate-Management"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Create Address Table
CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code VARCHAR(20),
    latitude NUMERIC,
    longitude NUMERIC
);

-- Create Client Table
CREATE TABLE Client (
    client_id SERIAL PRIMARY KEY,
    client_name VARCHAR(255),
    client_gender VARCHAR(20),
    client_phone VARCHAR(20),
    client_email VARCHAR(255),
    client_dob DATE,
    address_id INT REFERENCES Address(address_id)
);

-- Create Agent Table
CREATE TABLE Agent (
    agent_id SERIAL PRIMARY KEY,
    agent_name VARCHAR(255),
    agent_gender VARCHAR(20),
    agent_phone VARCHAR(20),
    agent_email VARCHAR(255),
    agent_dob DATE,
    address_id INT REFERENCES Address(address_id),
    hire_date DATE,
    title VARCHAR(100)
);

-- Create Owner Table
CREATE TABLE Owner (
    owner_id SERIAL PRIMARY KEY,
    owner_name VARCHAR(255),
    owner_gender VARCHAR(20),
    owner_phone VARCHAR(20),
    owner_email VARCHAR(255),
    owner_dob DATE,
    address_id INT REFERENCES Address(address_id)
);

-- Create Features Table
CREATE TABLE Features (
    feature_id SERIAL PRIMARY KEY,
    lot_area_sqft INT,
    no_bedrooms INT,
    no_bathrooms INT,
    no_kitchens INT,
    no_floors INT,
    parking_area_sqft INT,
    year_built INT,
    condition_rating INT
);

-- Create Property Table
CREATE TABLE Property (
    property_id SERIAL PRIMARY KEY,
    address_id INT UNIQUE REFERENCES Address(address_id),
    owner_id INT REFERENCES Owner(owner_id),
    agent_id INT REFERENCES Agent(agent_id),
    feature_id INT REFERENCES Features(feature_id),
    listing_date DATE,
    listing_type VARCHAR(50),
    asking_amount NUMERIC
);

-- Maintenance Table
CREATE TABLE Maintenance (
    maintenance_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES Property(property_id),
    maintenance_date DATE,
    maintenance_type VARCHAR(100),
    cost NUMERIC,
    description TEXT
);

-- Create Visit Table
CREATE TABLE Visit (
    visit_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES Property(property_id),
    visit_date DATE,
    client_id INT REFERENCES Client(client_id),
    description TEXT
);

-- Create Commission Table
CREATE TABLE Commission (
    commission_id SERIAL PRIMARY KEY,
    commission_rate NUMERIC,
    commission_amount NUMERIC,
    payment_method VARCHAR(50),
    payment_date DATE
);

-- Create Sale Table
CREATE TABLE Sale (
    sale_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES Property(property_id),
    sale_date DATE,
    client_id INT REFERENCES Client(client_id),
    commission_id INT REFERENCES Commission(commission_id),
    sale_amount NUMERIC
);

-- Create Contract Table
CREATE TABLE Contract (
    contract_id SERIAL PRIMARY KEY,
    contract_terms TEXT
);

-- Create Rent Table
CREATE TABLE Rent (
    rent_id SERIAL PRIMARY KEY,
    property_id INT REFERENCES Property(property_id),
    agreement_date DATE,
    rent_start_date DATE,
    rent_end_date DATE,
    rent_amount NUMERIC,
    client_id INT REFERENCES Client(client_id),
    commission_id INT REFERENCES Commission(commission_id),
    contract_id INT REFERENCES Contract(contract_id)
);

-- Create Admin Table
CREATE TABLE Admin (
    admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(255),
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);
