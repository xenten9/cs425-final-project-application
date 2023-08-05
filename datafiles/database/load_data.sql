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

