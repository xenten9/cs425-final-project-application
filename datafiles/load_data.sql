DROP DATABASE matthew_family_realty;

# Create database
CREATE DATABASE matthew_family_realty;
USE matthew_family_realty;

# Create tables
CREATE TABLE person(
	person_id INT,
    first_name VARCHAR(40),
    last_name VARCHAR(60),
    date_of_birth DATE,
    is_employed BOOL,
    PRIMARY KEY (person_id)
);

CREATE TABLE personal_emails(
	person_id INT,
    email VARCHAR(256),
	PRIMARY KEY (person_id, email),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);

CREATE TABLE client(
	client_id INT,
    realtor_id INT,
    person_id INT,
	PRIMARY KEY (client_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);

CREATE TABLE employee(
	employee_id INT,
    join_date DATE,
    commission NUMERIC(9,2),
    hours_worked INT,
    hourly_rate NUMERIC(5,2),
    work_email VARCHAR(256),
    person_id INT,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);

CREATE TABLE manager(
    manager_id INT,
    status VARCHAR(20),
    employee_id INT,
    PRIMARY KEY (manager_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)    
);

CREATE TABLE realtor(
    realtor_id INT,
    meetings_to_date SMALLINT,
    manager_id INT,
    employee_id INT,
    PRIMARY KEY (realtor_id),
    FOREIGN KEY (manager_id) REFERENCES manager(manager_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)    
);

CREATE TABLE residence(
    residence_id INT,
    expected_price NUMERIC(11, 2),
    date_of_purchase DATE,
    is_lease BOOL,
    square_footage SMALLINT,
    bed_count SMALLINT,
    steet_number INT,
    street_name VARCHAR(60),
    zip_code INT,
    city VARCHAR(60),
    state VARCHAR(60),
    country VARCHAR(3),
    bath_count SMALLINT,
    kitchen SMALLINT,
    utilities VARCHAR(20),
    smoking BOOL,
    expected_rent NUMERIC(9, 2),
    pets VARCHAR(80),
    notes VARCHAR(140),
    person_id INT,
    realtor_id INT,
    client_id INT,
    PRIMARY KEY (residence_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (realtor_id) REFERENCES realtor(realtor_id),
    FOREIGN KEY (client_id) REFERENCES client(client_id)
);

CREATE TABLE wants_to_buy(
    client_id INT,
    residence_id INT,
    rating SMALLINT,
    comments VARCHAR(140),
    PRIMARY KEY (client_id, residence_id),
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (residence_id) REFERENCES residence(residence_id)
);

CREATE TABLE apartment_complex(
    apartment_id INT,
    is_dorm BOOL,
    PRIMARY KEY (apartment_id)
);

CREATE TABLE apartment_suite(
    suite_id INT,
    room_number SMALLINT,
    floor SMALLINT,
    apartment_id INT,
    residence_id INT,
    PRIMARY KEY (suite_id),
    FOREIGN KEY (apartment_id) REFERENCES apartment_complex(apartment_id),
    FOREIGN KEY (residence_id) REFERENCES residence(residence_id)
);

CREATE TABLE house(
    house_id INT,
    air_conditioning VARCHAR(20),
    has_gas BOOL,
    floor_count SMALLINT,
    house_ownership_association VARCHAR(80),
    residence_id INT,
    PRIMARY KEY (house_id),
    FOREIGN KEY (residence_id) REFERENCES residence(residence_id)
);

CREATE TABLE single_family_house(
    single_family_house_id INT,
    garage_count SMALLINT,
    house_id INT,
    PRIMARY KEY (single_family_house_id),
    FOREIGN KEY (house_id) REFERENCES house(house_id)
);

CREATE TABLE duplex(
    duplex_id INT,
    has_post_box BOOL,
    has_laundry BOOL,
    house_id INT,
    PRIMARY KEY (duplex_id),
    FOREIGN KEY (house_id) REFERENCES house(house_id)
);

# Populate tables with data
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/person.csv'
INTO TABLE person
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';'
(person_id, first_name, last_name, @birth_date_data, is_employed)
SET date_of_birth  = STR_TO_DATE(@birth_date_data, '%Y-%c-%e');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/emails.csv'
INTO TABLE personal_emails
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/clients.csv'
INTO TABLE client
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/employees.csv'
INTO TABLE employee
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';'
(employee_id, @join_date_data, commission, hours_worked, hourly_rate, work_email, person_id)
SET join_date  = STR_TO_DATE(@join_date_data, '%Y-%c-%e');

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/managers.csv'
INTO TABLE manager
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/realtors.csv'
INTO TABLE realtor
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/residences.csv'
INTO TABLE residence
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/houses.csv'
INTO TABLE house
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/apartment_complexes.csv'
INTO TABLE apartment_complex
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/apartment_suites.csv'
INTO TABLE apartment_suite
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/single_family_houses.csv'
INTO TABLE single_family_house
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/duplexes.csv'
INTO TABLE duplex
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/wants_to_buy.csv'
INTO TABLE wants_to_buy
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY ';';

# TEST
SELECT person.person_id, first_name, last_name, date_of_birth, is_employed, email
FROM person LEFT OUTER JOIN personal_emails ON person.person_id = personal_emails.person_id;

SELECT *
FROM person
LIMIT 1000;

SELECT *
FROM employee NATURAL JOIN person
LIMIT 150;

WITH big AS (SELECT person_id, employee.employee_id, hourly_rate, status, manager_id FROM employee LEFT JOIN manager ON employee.employee_id = manager.employee_id)
SELECT *
FROM person, big
WHERE person.person_id = big.person_id;

SELECT manager_id, COUNT(manager_id)
FROM realtor
GROUP BY manager_id;

SELECT * FROM client
LIMIT 500;

SELECT realtor_id, COUNT(realtor_id)
FROM client NATURAL JOIN realtor
GROUP BY realtor_id
LIMIT 500;

SELECT *
FROM house
LIMIT 1000;

SELECT *
FROM apartment_suite
LIMIT 1000;

SELECT *
FROM single_family_house
LIMIT 1000;

SELECT *
FROM duplex
LIMIT 1000;

SELECT *
FROM single_family_house NATURAL JOIN duplex;

SELECT *
FROM wants_to_buy NATURAL JOIN residence
LIMIT 1000;

/*----------------------------------------------------------------------------------------------------------------------------------------------------------------------*/
#SQL Commands

#List of Realtors who are clients
SELECT realtor.realtor_id, client.client_id, first_name, last_name
FROM realtor, client, person, employee
WHERE realtor.employee_id = employee.employee_id
AND employee.person_id = client.person_id
AND employee.person_id = person.person_id;

#List of Houses with gas, pets, and water
SELECT house_id, has_gas, pets, utilities
FROM residence, house
WHERE has_gas = 1
AND pets NOT LIKE "None"
AND utilities LIKE "%W%"
AND house.residence_id = residence.residence_id;

#List of houses with rent < 5,000 sorted descending in price
SELECT house_id, expected_rent
FROM house, residence
WHERE expected_rent <= 5000
AND house.residence_id = residence.residence_id
ORDER BY expected_rent DESC
LIMIT 1000;

#List of top 20 earning employees
SELECT employee_id, first_name, last_name, hourly_rate * hours_worked + commission as earnings
FROM person, employee
WHERE employee.person_id = person.person_id
ORDER BY earnings
LIMIT 20;

#List of Apartment complex with more than 30 apartments
SELECT apartment_id, COUNT(suite_id)
FROM apartment_complex NATURAL JOIN apartment_suite
GROUP BY apartment_id
HAVING COUNT(suite_id) > 30;

#List of Residential Homes in North Carolina ordered by expected price increasing
SELECT *
FROM Residence
WHERE state LIKE "Nor%Car%"
ORDER BY expected_price ASC;

#Name of person who owns a specific house
SELECT first_name, last_name, residence_id, expected_price
FROM person NATURAL JOIN residence
WHERE first_name LIKE "M%s";

#Employee with highest hours worked and their percent rank of hourly_rate
WITH fancy_percent AS (
    SELECT employee_id, ROUND(PERCENT_RANK() OVER (ORDER BY hourly_rate) * 100, 2) as percentage_rank
    FROM employee NATURAL JOIN person
)
SELECT first_name, last_name, employee_id, hours_worked, percentage_rank
FROM employee NATURAL JOIN person NATURAL JOIN fancy_percent
WHERE hours_worked >= all (
    SELECT hours_worked FROM employee
);

#List the expected price of houses associated with home ownership association “New Leaf” and cheaper than the average expected price of all houses, and who owns them
SELECT house_id, expected_price, house_ownership_association
FROM house NATURAL JOIN residence
WHERE expected_price <= all (SELECT AVG(expected_price) FROM house NATURAL JOIN residence)
AND house_ownership_association = "New Leaf";

