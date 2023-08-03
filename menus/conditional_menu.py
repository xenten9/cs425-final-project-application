import tkinter as tk
import tkinter.messagebox as popup

from constants import *
from menus.order_menu import OrderMenu
from sql import Sql
from tk_manager import TkManager


class ConditionalMenu(tk.Frame):
    def __init__(self, root: TkManager, *args, **kwargs):
        super().__init__(root.root, *args, **kwargs)
        self.root = root

    def create(self):
        query = Sql.get().get_active_query()
        tables = query.get_tables()

        self.root.create_frame("conditional_menu", self)

        # Title
        tk.Label(self, text="Form conditionals", **FONT_MEDIUM).pack(
            **{**PACK_FILL_X, **PACK_TOP}
        )

        # Conditonal creation grid
        conditional_grid = tk.Frame(self, bg="pink")

        for i in range(5):
            conditional_grid.grid_columnconfigure(i, weight=1)

        available_attributes: list[str] = []
        for table in tables:
            available_attributes.extend(
                [
                    f"{table}.{attribute}"
                    for attribute in Sql.get().table_attributes[table]
                ]
            )

        available_operators = ["=", "!=", "<", "<=", ">", ">=", "LIKE", "REGEXP"]
        available_joins = ["", "OR", "AND"]

        for i in range(10):
            operand_1 = tk.StringVar(value="")
            operator = tk.StringVar(value="=")
            operand_2 = tk.StringVar(value="")
            custom_2 = tk.StringVar(value="")
            logical_join = tk.StringVar(value="")
            query.conditional_vars.append(
                (
                    operand_1,
                    operator,
                    operand_2,
                    custom_2,
                    logical_join,
                )
            )

            widget_operand_1 = tk.OptionMenu(
                conditional_grid,
                operand_1,
                *["", *available_attributes],
            )
            widget_operand_1.grid(row=i, column=0, **GRID_FILL_X)
            widget_operand_1.config(**FONT_SMALL)

            # Operator
            widget_operator = tk.OptionMenu(
                conditional_grid, operator, *available_operators
            )
            widget_operator.grid(row=i, column=1, **GRID_FILL_X)
            widget_operator.config(**FONT_SMALL)

            # Operand 2
            widget_custom_2 = tk.Entry(
                conditional_grid, textvariable=custom_2, state="disabled", **FONT_SMALL
            )
            widget_custom_2.grid(row=i, column=3, **GRID_FILL_X)
            widget_operand_2 = tk.OptionMenu(
                conditional_grid,
                operand_2,
                command=lambda x, widget=widget_custom_2: widget.configure(
                    {"state": "normal"}
                )
                if x == "custom"
                else widget.configure({"state": "disabled"}),
                *["", "custom", *available_attributes],
            )
            widget_operand_2.grid(row=i, column=2, **GRID_FILL_X)
            widget_operand_2.config(**FONT_SMALL)

            # Logical join
            widget_logical_join = tk.OptionMenu(
                conditional_grid, logical_join, *available_joins
            )
            widget_logical_join.grid(row=i, column=4, **GRID_FILL_X)
            widget_logical_join.config(**FONT_SMALL)
        widget_logical_join.config(state="disabled")  # disables last join

        # Pack conditionals
        conditional_grid.pack(**{**PACK_FILL_BOTH, **PACK_TOP})

        # Proceed button
        button_frame = tk.Frame(self)
        button_frame.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        tk.Button(
            button_frame,
            text="Proceed",
            command=self.goto_next,
            **FONT_MEDIUM,
        ).grid(row=0, column=1, **{**GRID_FILL_X})
        tk.Button(
            button_frame,
            text="Go back",
            command=self.goto_prev,
            **FONT_MEDIUM,
        ).grid(row=0, column=0, **{**GRID_FILL_X})

    def goto_next(self):
        root = self.root

        root.destroy_frame("order_menu")
        order_menu = OrderMenu(root)
        order_menu.create()
        root.pack("order_menu")

    def goto_prev(self):
        self.root.pack("attribute_menu")
