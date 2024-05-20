CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    flight_number VARCHAR(50) NOT NULL,
    departure_date DATE NOT NULL,
    booking_class VARCHAR(50) NOT NULL,
    available_seats INTEGER NOT NULL,
    time TIME NOT NULL,
    UNIQUE (flight_number, booking_class)
);