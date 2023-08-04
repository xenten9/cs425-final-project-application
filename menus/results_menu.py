from datetime import date
from decimal import Decimal
import json
import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

from constants import *
from sql import Sql
from tk_manager import TkManager


class ResultsMenu(tk.Frame):
    def __init__(self, manager: TkManager, *args, **kwargs):
        super().__init__(manager.root, *args, **kwargs)
        self.manager = manager

    def create(self):
        query = Sql.get().get_active_query()
        results = Sql.get().get_results()

        self.manager.create_frame("results_menu", self)

        # External UI
        tk.Label(self, text="Results", bg="#FFD", **FONT_MEDIUM_BOLD).pack(
            **{**PACK_TOP, **PACK_FILL_X}
        )

        button_frame = tk.Frame(self)
        button_frame.pack(**{**PACK_BOTTOM, **PACK_FILL_X})

        tk.Button(
            button_frame,
            text="Go back",
            command=self.goto_prev,
            **FONT_MEDIUM,
        ).pack(**{**PACK_LEFT, **PACK_FILL_X, **SMALL_PAD})
        tk.Button(
            button_frame,
            text="Save query to disk",
            command=self.save_query,
            **FONT_MEDIUM,
        ).pack(**{**PACK_LEFT, **PACK_FILL_X, **SMALL_PAD})

        # Table for results
        frame_table_container = tk.Frame(self, bg="#228")
        canvas = tk.Canvas(frame_table_container, height=10000, bg="#CCC")
        frame_table = tk.Frame(canvas, bg="#000", **SMALL_PAD)

        # Create and bind scroll bars
        yscrollbar = tk.Scrollbar(
            frame_table_container, orient="vertical", command=canvas.yview
        )
        yscrollbar.pack(**{**PACK_FILL_Y, **PACK_RIGHT})
        canvas.configure(yscrollcommand=yscrollbar.set)

        xscrollbar = tk.Scrollbar(
            frame_table_container, orient="horizontal", command=canvas.xview
        )
        xscrollbar.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        canvas.configure(xscrollcommand=xscrollbar.set)

        # Create window for frame table in canvas
        canvas.create_window((0, 0), window=frame_table, anchor="nw")

        tk.Label(frame_table, text="result #", **FONT_SMALL_BOLD).grid(
            row=0, column=0, **{**SMALL_PAD, **GRID_FILL_X}
        )

        for i, attribute in enumerate(query.get_ordered_attributes()):
            tk.Label(frame_table, text=attribute, **FONT_SMALL_BOLD).grid(
                row=0, column=i + 1, **{**SMALL_PAD, **GRID_FILL_X}
            )

        for i, result in enumerate(results):
            tk.Label(
                frame_table, text=str(i + 1), **{**FONT_SMALL, **RIGHT_ALIGN}
            ).grid(row=i + 1, column=0, **{**SMALL_PAD, **GRID_FILL_X})
            for j, cell in enumerate(result):
                if isinstance(cell, date):
                    cell = f"{cell.month}/{cell.day}/{cell.year}"
                elif isinstance(cell, Decimal):
                    cell = float(cell)
                    cell = "{:,.2f}".format(cell)
                tk.Label(frame_table, text=cell, **FONT_SMALL).grid(
                    row=i + 1, column=j + 1, **{**SMALL_PAD, **GRID_FILL_X}
                )

        # Packing events
        canvas.pack(expand=True, **{**PACK_TOP, **PACK_FILL_BOTH})
        frame_table_container.pack(**PACK_FILL_BOTH)

        # Set scroll region
        canvas.update()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    def goto_next(self):
        pass

    def save_query(self):
        query = Sql.get().active_query
        query_dict = dict()
        query_dict["attributes"] = query.get_attributes()
        query_dict["tables"] = query.get_tables()
        query_dict["conditionals"] = query.get_conditionals()
        query_dict["order"] = query.get_ordered_attributes()
        query_dict["use_natural_join"] = query.use_natural_join.get()
        file_name = asksaveasfilename(initialdir="./queries", defaultextension=".query", filetypes=[("Query file", "*.query")])
        if not file_name.endswith(".query"):
            file_name += ".query"
        if file_name:
            if os.path.isfile(file_name):
                os.remove(file_name)
            with open(file_name, "x") as file_handle:
                json.dump(query_dict, file_handle, indent=4)

    def goto_prev(self):
        self.manager.pack("order_menu")
