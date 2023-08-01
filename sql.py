import pymysql
import tkinter.messagebox as popup


class SQL_Interface:
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

    def query(
        self,
        tables: list[str],
        attributes: list[list[bool]],
        conditionals: list[tuple[str, str, str, str, str]],
    ):
        new_attributes = []
        for i, table in enumerate(tables):
            for j in range(len(attributes[i])):
                if attributes[i][j]:
                    new_attributes.append(self.table_attributes[table][j])
        new_attributes = list(set(new_attributes))

        command = ""
        command += f"SELECT {', '.join(new_attributes)}\n"
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
                    popup.showinfo(
                        "ERROR", "Opperand 1 must be specified"
                    )
                    return []

                first_table, attribute_1 = operand_1.split(".")
                type_1 = self.table_types[first_table][attribute_1]

                pytype_1 = type_1.strip("()0123456789,")
                pytype_1 = pytype_dict[pytype_1]

                # Operator limits
                if operator in ("LIKE", "REGEXP"):
                    if pytype_1 != str:
                        popup.showinfo(
                            "ERROR", f"Non string operand <{operand_1}> cannot use operator <{operator}>"
                        )
                        return []

                # Operand typing
                table_2, attribute_2 = operand_2.split(".")
                type_2 = self.table_types[table_2][attribute_2]
                pytype_2 = type_2.strip("()0123456789,")
                pytype_2 = pytype_dict[pytype_2]
                if operand_2 == "custom":
                    arguments.append(pytype_2(custom))
                    operand_2 = "%s"
                elif operand_2 == "":
                    popup.showinfo(
                        "ERROR", "Opperand 2 must be specified"
                    )
                    return []
                elif pytype_1 != pytype_2:
                    popup.showinfo(
                        "ERROR", f"<{operand_1}> does not match type of <{operand_2}>"
                    )
                    return []
                command += f"{operand_1} {operator} {operand_2}"

                if join == "":
                    break
                else:
                    command += f"\n{join} "

        command += ";"

        print(self.cursor.mogrify(command, arguments))

        self.cursor.execute(command, arguments)

        return self.cursor.fetchall()
