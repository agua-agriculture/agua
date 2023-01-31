DROP SCHEMA IF EXISTS agua CASCADE;
CREATE SCHEMA agua;
SET search_path TO agua;

CREATE TABLE farmer (
    farmer_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    total_message_sent INTEGER NOT NULL DEFAULT 0,
);

CREATE TABLE weather (
    weather_id SERIAL PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    rainfall FLOAT NOT NULL,
);

CREATE TABLE crop (
    crop_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    farmer_id INTEGER NOT NULL REFERENCES farmer(farmer_id),
    required_water_per_hectare FLOAT NOT NULL,
    total_area FLOAT NOT NULL,
);

CREATE TABLE recommended_irrigation (
    farmer_id INTEGER NOT NULL REFERENCES farmer(farmer_id),
    crop_id INTEGER NOT NULL REFERENCES crop(crop_id),
    weather_id INTEGER NOT NULL REFERENCES weather(weather_id),
    date TIMESTAMP NOT NULL,
    recommended_irrigation FLOAT NOT NULL,
    PRIMARY KEY (farmer_id, crop_id, date, weather_id)
);

CREATE TABLE required_irrigation (
    farmer_id INTEGER NOT NULL REFERENCES farmer(farmer_id),
    crop_id INTEGER NOT NULL REFERENCES crop(crop_id),
    date TIMESTAMP NOT NULL,
    irrigation_used FLOAT NOT NULL,
    PRIMARY KEY (farmer_id, crop_id, date)
);