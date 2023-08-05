from __future__ import annotations
import getpass

import pymysql
import tkinter.messagebox as popup
import tkinter as tk


class Query:
    def __init__(self) -> None:
        self.table_vars: dict[str, tk.BooleanVar] = {
            table: tk.BooleanVar() for table in Sql.get().tables
        }
        self.attribute_vars: dict[str, dict[str, tk.BooleanVar]]
        self.conditional_vars: list[
            tuple[tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar, tk.StringVar]
        ] = []
        self.ordering_vars: dict[str, tk.StringVar]
        self.use_natural_join = tk.BooleanVar(value=1)

    def update_attributes(self):
        self.attribute_vars: dict[str, dict[str, tk.BooleanVar]] = {
            table: {
                attribute: tk.BooleanVar()
                for attribute in Sql.get().table_attributes[table]
            }
            for table in Sql.get().tables
        }

    def update_ordering(self):
        list_of_attributes = []
        for table in self.get_tables():
            list_of_attributes.extend(self.get_attributes()[table])
        self.ordering_vars: dict[str, tk.StringVar] = {
            attribute: tk.StringVar() for attribute in list_of_attributes
        }

    def get_tables(self) -> list[str]:
        return list(
            filter(
                lambda x: x,
                [
                    table if var.get() else None
                    for table, var in self.table_vars.items()
                ],
            )
        )

    def get_attributes(self) -> dict[str, list[str]]:
        return {
            table: list(
                filter(
                    lambda x: x,
                    [
                        attribute if var.get() else None
                        for attribute, var in self.attribute_vars[table].items()
                    ],
                )
            )
            for table in self.get_tables()
        }

    def get_conditionals(self) -> list[tuple[str, str, str, str, str]]:
        return [tuple([var.get() for var in row]) for row in self.conditional_vars]

    def get_ordered_attributes(self) -> list[str]:
        out = [None] * len(self.ordering_vars)
        for attribute, var in self.ordering_vars.items():
            out[int(var.get()) - 1] = attribute
        return out


class Sql:
    _instance = None

    def __init__(self) -> None:
        self.active_query = None
        self._results = None

        # Access database
        try:
            with open("./password") as file:
                password = file.read()
        except FileNotFoundError:
            password = getpass.getpass("Password: ")

        # Use database
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password=password,
            database="matthew_family_realty",
        )
        self.cursor = self.connection.cursor()

        # Get list of tables
        self.cursor.execute(  # Get all tables
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE' AND table_schema="matthew_family_realty"
            ORDER BY table_name;
            """
        )
        self.tables = [str(table[0]) for table in self.cursor]

        self.table_attributes: dict[str, list[str]] = dict()
        self.table_types: dict[str, dict[str, str]] = dict()
        for table in self.tables:
            self.table_attributes[table] = []
            self.table_types[table] = dict()
            self.cursor.execute(  # Get all column names from table
                f"""
                SHOW COLUMNS
                FROM {table};
                """
            )
            for row in self.cursor:
                self.table_attributes[table].append(row[0])
                self.table_types[table][row[0]] = row[1]

    def create_query(self):
        self.active_query = Query()

    def query(self) -> tuple:
        query = self.get_active_query()
        attributes = query.get_ordered_attributes()
        tables = query.get_tables()
        conditionals = query.get_conditionals()
        command = ""
        if query.use_natural_join.get():
            command += f"SELECT {', '.join(attributes)}\n"
            command += f"FROM {' NATURAL JOIN '.join(tables)}"
        else:
            for i, attribute in enumerate(attributes):
                table = next(
                    filter(
                        lambda x: x,
                        [
                            table if attribute in self.table_attributes[table] else None
                            for table in tables
                        ],
                    )
                )

                attributes[i] = f"{table}.{attribute}"

            command += f"SELECT {', '.join(attributes)}\n"
            command += f"FROM {', '.join(tables)}"

        arguments = []

        if conditionals[0][0] != "":
            command += "\nWHERE "

            pytype_dict: dict[str, type] = {
                "decimal": float,
                "tinyint": int,
                "varchar": str,
                "smallint": int,
                "int": int,
                "date": str,  # maybe change this
            }

            for row in conditionals:
                operand_1, operator, operand_2, custom, join = row

                if operand_1 == "":
                    popup.showinfo("ERROR", "Opperand 1 must be specified!")
                    return

                first_table, attribute_1 = operand_1.split(".")
                type_1 = self.table_types[first_table][attribute_1]

                pytype_1 = type_1.strip("()0123456789,")
                pytype_1 = pytype_dict[pytype_1]

                # Operator limits
                if operator in ("LIKE", "REGEXP"):
                    if pytype_1 != str:
                        popup.showinfo(
                            "ERROR",
                            f"Non string operand <{operand_1}> cannot use operator <{operator}>!",
                        )
                        return

                # Operand typing
                if operand_2 == "custom":
                    arguments.append(pytype_1(custom))
                    operand_2 = "%s"
                elif operand_2 == "":
                    popup.showinfo("ERROR", "Opperand 2 must be specified!")
                    return
                else:
                    table_2, attribute_2 = operand_2.split(".")
                    type_2 = self.table_types[table_2][attribute_2]
                    pytype_2 = type_2.strip("()0123456789,")
                    pytype_2 = pytype_dict[pytype_2]
                    if pytype_1 != pytype_2:
                        popup.showinfo(
                            "ERROR",
                            f"<{operand_1}> does not match type of <{operand_2}>!",
                        )
                        return

                # Finish command
                command += f"{operand_1} {operator} {operand_2}"

                # Is there more conditionals
                if join == "":
                    break
                else:
                    command += f"\n{join} "

        # Finalize command
        command += ";"
        print(self.cursor.mogrify(command, arguments))

        self.cursor.execute(command, arguments)

        self._results = self.cursor.fetchall()

    def get():
        if not Sql._instance:
            Sql._instance = Sql()
        return Sql._instance

    def get_active_query(self) -> Query:
        return self.active_query

    def get_results(self) -> tuple:
        return self._results
