import sys
from sql import Sql

HELP = """
    --help or -h: show list of possible command line arguments.
    --limit: limit number of tuples returned for each query.
    --skip: comma-sepperated no-space list of numbers to skip the corresponding command,
        IE: <--skip 1,3,4> will skip the first third and fourth commands.
    --show: comma-sepperated no-space list of numbers to show the corresponding command,
        NOTE: skip overides show, by deafult all commands are shown.
        IE: <--show 2,5,7> will show the second fifth and seventh commands.
"""

PROMPTS = [
    "List of Realtors who are clients",
    "List of Houses with gas, pets, and water",
    "List of houses with rent < 5,000 sorted descending in price",
    "List of top 20 earning employees",
    "List of Apartment complex with more than 30 apartments",
    "List of Residential Homes in North Carolina ordered by expected price increasing",
    "Name of person who owns a specific house",
    "Find any times when a single family house Shares the house ID with a Duplex House",
    "Employee with highest hours worked and their percent rank of hourly_rate",
    "List the expected price of houses associated with home ownership association “New Leaf” and cheaper than the average expected price of all houses, and who owns them",
]

COMMANDS = [
    ##List of Realtors who are clients
    """
    SELECT realtor.realtor_id, client.client_id, first_name, last_name
    FROM realtor, client, person, employee
    WHERE realtor.employee_id = employee.employee_id
    AND employee.person_id = client.person_id
    AND employee.person_id = person.person_id;
    """,

    ##List of Houses with gas, pets, and water
    """
    SELECT house_id, has_gas, pets, utilities
    FROM residence, house
    WHERE has_gas = 1
    AND pets NOT LIKE "None"
    AND utilities LIKE "%W%"
    AND house.residence_id = residence.residence_id;
    """,

    ##List of houses with rent < 5,000 sorted descending in price
    """
    SELECT house_id, expected_rent
    FROM house, residence
    WHERE expected_rent <= 5000
    AND house.residence_id = residence.residence_id
    ORDER BY expected_rent DESC
    LIMIT 1000;
    """,

    ##List of top 20 earning employees
    """
    SELECT employee_id, first_name, last_name, hourly_rate * hours_worked + commission as earnings
    FROM person, employee
    WHERE employee.person_id = person.person_id
    ORDER BY earnings
    LIMIT 20;
    """,

    ##List of Apartment complex with more than 30 apartments
    """
    SELECT apartment_id, COUNT(suite_id)
    FROM apartment_complex NATURAL JOIN apartment_suite
    GROUP BY apartment_id
    HAVING COUNT(suite_id) > 30;
    """,

    ##List of Residential Homes in North Carolina ordered by expected price increasing
    """
    SELECT *
    FROM Residence
    WHERE state LIKE "Nor%Car%"
    ORDER BY expected_price ASC;
    """,

    ##Name of person who owns a specific house
    """
    SELECT first_name, last_name, residence_id, expected_price
    FROM person NATURAL JOIN residence
    WHERE first_name LIKE "M%s";
    """,

    #Find any times when a single family house Shares the house ID with a Duplex House
    """
    SELECT *
    FROM single_family_house NATURAL JOIN duplex;
    """,

    #Employee with highest hours worked and their percent rank of hourly_rate
    """
    WITH fancy_percent AS (
        SELECT employee_id, ROUND(PERCENT_RANK() OVER (ORDER BY hourly_rate) * 100, 2) as percentage_rank
        FROM employee NATURAL JOIN person
    )
    SELECT first_name, last_name, employee_id, hours_worked, percentage_rank
    FROM employee NATURAL JOIN person NATURAL JOIN fancy_percent
    WHERE hours_worked >= all (
        SELECT hours_worked FROM employee
    );
    """,

    #List the expected price of houses associated with home ownership association “New Leaf” and cheaper than the average expected price of all houses, and who owns them
    """
    SELECT house_id, expected_price, house_ownership_association
    FROM house NATURAL JOIN residence
    WHERE expected_price <= all (SELECT AVG(expected_price) FROM house NATURAL JOIN residence)
    AND house_ownership_association = "New Leaf";
    """,
]


def main(limit: int, skip: list[int], show: list[int]):
    cursor = Sql.get().cursor

    for i, command in enumerate(COMMANDS):
        if i + 1 in show and i + 1 not in skip: # Check for skipping and showing
            # Run sql command
            cursor.execute(command)
            print(f"{'-'*10} command {i + 1} {'-'*10}")
            print(PROMPTS[i] + ":")
            print(command)

            if limit == -1: # No limit
                result = cursor.fetchall()
            else: # Limit
                result = cursor.fetchmany(min(limit, cursor.rowcount))

            # Print results
            for row in result:
                print(row)
            
            print("\n")


if __name__ == "__main__":
    limit = -1
    skip = []
    show = list(range(1, 101))
    try:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])
    except ValueError:
        pass
    try:
        skip = list(
            map(lambda x: int(x), sys.argv[sys.argv.index("--skip") + 1].split(","))
        )
    except ValueError:
        pass
    try:
        show = list(
            map(lambda x: int(x), sys.argv[sys.argv.index("--show") + 1].split(","))
        )
    except ValueError:
        pass

    try:
        sys.argv.index("--help")
    except ValueError:
        try:
            sys.argv.index("-h")
        except ValueError:
            main(limit, skip, show)
        else:
            print(HELP)
    else:
        print(HELP)
