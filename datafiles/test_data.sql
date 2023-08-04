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

#Find any times when a single family house Shares the house ID with a Duplex House
SELECT *
FROM single_family_house NATURAL JOIN duplex;

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

