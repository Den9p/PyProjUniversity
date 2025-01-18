CREATE TABLE airplane
(
	airplane_id varchar(5) PRIMARY KEY,
	airplane_type text NOT NULL,
	airplane_speed int NOT NULL,
	airplane_hight int NOT NULL,
	airplane_capacity int NOT NULL
);

CREATE TABLE client
(
    client_passport_id varchar(10) PRIMARY KEY,
    client_name varchar(20) NOT NULL,
    client_surname varchar(30) NOT NULL,
    client_patronymic varchar(30),
    password_hash varchar(128) NOT NULL,
    salt varchar(128) NOT NULL
);

CREATE TABLE flight
(
	flight_name varchar(6) PRIMARY KEY,
	flight_departure text NOT NULL,
	flight_arrival text NOT NULL,
	timestamp_departure timestamp NOT NULL,
	timestamp_arrival timestamp NOT NULL,
	ticket_price int NOT NULL,
	fk_airplane_id varchar(5) REFERENCES airplane(airplane_id)
);

CREATE TABLE client_flight
(
    client_passport_id varchar(10) REFERENCES client(client_passport_id),
    flight_name varchar(6) REFERENCES flight(flight_name),
    ticket_number varchar(12) UNIQUE,
    CONSTRAINT client_flight_pkey PRIMARY KEY (client_passport_id, flight_name)
);
