CREATE SCHEMA IF NOT EXISTS dummy;

CREATE TABLE IF NOT EXISTS dummy.cars (
    car_id SERIAL PRIMARY KEY,
    brand VARCHAR(255),
    model VARCHAR(255),
    is_available BOOLEAN DEFAULT false
);

INSERT INTO dummy.cars VALUES (DEFAULT, 'Audi', 'A4', true);

CREATE TABLE IF NOT EXISTS dummy.users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100)
);
INSERT INTO dummy.users VALUES (DEFAULT, 'Some Name', 'Some Surname');