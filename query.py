import tkinter as tk

from sql import Sql


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
