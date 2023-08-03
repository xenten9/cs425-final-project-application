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

COMMANDS = [
    """
    SELECT * FROM employee;
    """,
    """
    SELECT * FROM manager;
    """,
]


def main(limit: int, skip: list[int], show: list[int]):
    cursor = Sql.get().cursor

    for i, command in enumerate(COMMANDS):
        if i + 1 in show and i + 1 not in skip: # Check for skipping and showing
            # Run sql command
            cursor.execute(command)
            print(f"{'-'*10} command {i + 1} {'-'*10}")
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
