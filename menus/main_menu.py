import json
from time import sleep
import tkinter as tk
from tkinter.filedialog import askopenfilename

from constants import *
from menus.attribute_menu import AttributeMenu
from menus.conditional_menu import ConditionalMenu
from menus.results_menu import ResultsMenu
from menus.table_menu import TableMenu
from tk_manager import TkManager
from sql import Sql


class MainMenu(tk.Frame):
    def __init__(self, manager: TkManager, *args, **kwargs) -> None:
        super().__init__(manager.root, *args, **kwargs)
        self.manager = manager

    def create(self):
        self.manager.create_frame("main_menu", self)

        # Title
        tk.Label(
            self, text="Matthew Family Real Estate Portal", **FONT_LARGE_BOLD, bg="#CFC"
        ).pack(**{**PACK_FILL_X, **PACK_TOP})

        # Main menu span
        span_frame = tk.Frame(self, bg="black")
        span_frame.pack(**{**PACK_CENTER})
        span_frame.columnconfigure(0, weight=1)
        for i in range(6):
            if i < 3:
                tk.Label(span_frame, **FONT_MEDIUM).grid(
                    row=i, column=0, **{**GRID_FILL_BOTH}
                )
            span_frame.rowconfigure(i, weight=1)
        tk.Button(
            span_frame, text="Proceed", command=self.goto_next, **FONT_MEDIUM
        ).grid(row=3, column=0, **{**GRID_FILL_BOTH, **SMALL_PAD})
        tk.Button(
            span_frame, text="Load Query", command=self.load_query, **FONT_MEDIUM
        ).grid(row=4, column=0, **{**GRID_FILL_BOTH, **SMALL_PAD})
        tk.Button(
            span_frame, text="Quit", command=self.manager.root.destroy, **FONT_MEDIUM
        ).grid(row=6, column=0, **{**GRID_FILL_BOTH, **SMALL_PAD})

        # Pack frames

    def goto_next(self):
        self.manager.destroy_frame("table_menu")
        attribute_table = TableMenu(self.manager)
        attribute_table.create()
        self.manager.pack("table_menu")

    def load_query(self):
        # file_dialog = FileDialog(self.manager.root, "Select query file")
        file_name = askopenfilename(
            initialdir="./queries",
            defaultextension=".query",
            filetypes=[("Query file", "*.query")],
        )
        print(file_name)
        # file = file_dialog.go("./queries", "*.query")
        if file_name:
            # Load file here
            contents: dict[
                str, bool | dict[list[str]] | list[str] | list[list[str]]
            ] = dict()
            with open(file_name, "r") as file_handle:
                contents: dict[
                    str, bool | dict[list[str]] | list[str] | list[list[str]]
                ] = json.load(file_handle)

            # Unpack
            attributes: dict[list[str]] = contents["attributes"]
            tables: list[str] = contents["tables"]
            conditionals: list[list[str]] = contents["conditionals"]
            order: list[str] = contents["order"]
            use_natural_join: bool = contents["use_natural_join"]

            # Reformat
            sql = Sql.get()
            query = sql.active_query

            self.manager.destroy_frame("table_menu")
            menu = TableMenu(self.manager)
            menu.create()

            for table in query.table_vars:
                query.table_vars[table].set(table in tables)
            query.use_natural_join.set(use_natural_join)

            menu = menu.goto_next()

            for table in attributes:
                for attribute in attributes[table]:
                    query.attribute_vars[table][attribute].set(True)

            menu = menu.goto_next()

            for i, conditional in enumerate(conditionals):
                for j, part in enumerate(conditional):
                    query.conditional_vars[i][j].set(part)

            menu = menu.goto_next()

            query.ordering_vars = {attribute: tk.StringVar() for attribute in order}
            for i, attribute in enumerate(order):
                query.ordering_vars[attribute].set(str(i + 1))

            menu = menu.goto_next()

    def goto_prev(self):
        pass
