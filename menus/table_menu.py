import tkinter as tk
import tkinter.messagebox as popup

from constants import *
from menus.attribute_menu import AttributeMenu
from sql import Sql
from tk_manager import TkManager
import numpy as np


class TableMenu(tk.Frame):
    def __init__(self, manager: TkManager, *args, **kwargs) -> None:
        super().__init__(manager.root, *args, **kwargs)
        self.manager = manager

    def create(self):
        query = Sql.get().get_active_query()

        self.manager.create_frame("table_menu", self, kwargs={"bg": "#B22"})

        # Title
        tk.Label(self, text="Select tables to query", **FONT_MEDIUM).pack(
            **{**PACK_FILL_X, **PACK_TOP}
        )

        # Accursed mess that is another checkbox grid
        check_boxes_frame = tk.Frame(self, padx=20, pady=20)

        for row, table in enumerate(Sql.get().tables):
            bool_var = query.table_vars[table]
            checkbox = tk.Checkbutton(
                check_boxes_frame,
                variable=bool_var,
                text=table,
                **FONT_SMALL,
            )
            checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

        # Use natural joins?
        bool_var = query.use_natural_join
        checkbox = tk.Checkbutton(
            check_boxes_frame,
            variable=bool_var,
            text="Use natural join?",
            **FONT_SMALL,
        )
        checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

        # Main menu span
        span_frame = tk.Frame(self)
        widgets: list[tk.Widget] = [
            tk.Button(
                span_frame,
                text="Reset selection",
                command=lambda: [var.set(0) for var in query.table_vars.values()],
                **FONT_SMALL,
            ),
            tk.Button(span_frame, text="Go back", command=self.goto_prev, **FONT_SMALL),
            tk.Button(span_frame, text="Proceed", command=self.goto_next, **FONT_SMALL),
        ]

        for i, widget in enumerate(widgets):
            widget.grid(row=0, column=i, **GRID_FILL_BOTH)
            span_frame.grid_columnconfigure(i, weight=1)

        # Pack frames
        span_frame.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        check_boxes_frame.pack(**{**PACK_TOP, **PACK_FILL_BOTH})

    def goto_next(self):
        query = Sql.get().get_active_query()
        tables = query.get_tables()

        # Conditions
        if len(tables) == 0:
            popup.showinfo("ERROR", "Must select at least one table!")
            return

        # Validate table connections for Natural Join
        if query.use_natural_join.get():
            # Form relation matrix
            mat: list[list[bool]] = []
            for i, table_0 in enumerate(tables):
                mat.append([])
                for table_1 in tables:
                    mat[i].append(
                        any(
                            (
                                attribute in Sql.get().table_attributes[table_0]
                                for attribute in Sql.get().table_attributes[table_1]
                            )
                        )
                    )

            # Check to see if all cells are accessible in n-1 (max required) steps
            if np.prod(np.mat(mat) ** (len(tables) - 1)) == 0:
                popup.showinfo("ERROR", "Tables cannot be natrual joined!")
                return

        self.manager.destroy_frame("attribute_menu")
        attribute_table = AttributeMenu(self.manager)
        attribute_table.create()
        self.manager.pack("attribute_menu")

    def goto_prev(self):
        self.manager.pack("main_menu")

