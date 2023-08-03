import tkinter as tk

from constants import *
from menus.table_menu import TableMenu
from tk_manager import TkManager


class MainMenu(tk.Frame):
    def __init__(self, manager: TkManager, *args, **kwargs) -> None:
        super().__init__(manager.root, *args, **kwargs)
        self.manager = manager

    def create(self):
        self.manager.create_frame("main_menu", self)

        # Title
        tk.Label(
            self, text="Matthew Family Real Estate Portal", **FONT_LARGE_BOLD
        ).pack(**{**PACK_FILL_X, **PACK_TOP})

        # Main menu span
        span_frame = tk.Frame(self)
        widgets: list[tk.Widget] = [
            # tk.Button(span_frame, text="Go back", command=self.goto_prev, **FONT_SMALL),
            tk.Button(span_frame, text="Proceed", command=self.goto_next, **FONT_SMALL),
        ]

        for i, widget in enumerate(widgets):
            widget.grid(row=0, column=i, **GRID_FILL_BOTH)
            span_frame.grid_columnconfigure(i, weight=1)

        # Pack frames
        span_frame.pack(**{**PACK_FILL_X, **PACK_BOTTOM})

    def goto_next(self):
        self.manager.destroy_frame("table_menu")
        attribute_table = TableMenu(self.manager)
        attribute_table.create()
        self.manager.pack("table_menu")

    def goto_prev(self):
        pass
