# from mysql import connector as con
import pymysql


class SQL_Interface:
    def __init__(self) -> None:
        # Access database
        file = open("./password")
        password = file.read()
        file.close()

        # Use database
        self.connection = pymysql.connect(host="localhost", user="root", password=password, database="matthew_family_realty")
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

        self.table_attributes = dict()
        for table in self.tables:
            self.cursor.execute(  # Get all column names from table
                f"""
                SHOW COLUMNS
                FROM {table};
                """
            )
            self.table_attributes[table] = [row[0] for row in self.cursor]

    def query(self, tables: list[str], attributes: list[list[bool]]):
        new_attributes = []
        for i, table in enumerate(tables):
            for j in range(len(attributes[i])):
                if attributes[i][j]:
                    new_attributes.append(self.table_attributes[table][j])
        command = ""
        command += f"SELECT {', '.join(new_attributes)}\n"
        command += f"FROM {' NATURAL JOIN '.join(tables)};"
        
        print(command)
        
        self.cursor.execute(command)
        
        return self.cursor.fetchall()

