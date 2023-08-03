from __future__ import annotations

import pymysql
import tkinter.messagebox as popup

#from query import Query


class Sql:
    _instance = None

    def __init__(self) -> None:
        # Access database
        file = open("./password")
        password = file.read()
        file.close()

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

    def query(self, query: "Query") -> tuple:
        attributes = query.get_ordered_attributes()
        tables = query.get_tables()
        conditionals = query.get_conditionals()
        command = ""
        command += f"SELECT {', '.join(attributes)}\n"
        command += f"FROM {' NATURAL JOIN '.join(tables)}"

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

        return self.cursor.fetchall()

    def get():
        if not Sql._instance:
            Sql._instance = Sql()
        return Sql._instance
