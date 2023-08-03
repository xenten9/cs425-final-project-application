import tkinter as tk
import tkinter.messagebox as popup

from constants import *
from menus.results_menu import ResultsMenu
from sql import Sql
from tk_manager import TkManager


class OrderMenu(tk.Frame):
    def __init__(self, manager: TkManager, *args, **kwargs):
        super().__init__(manager.root, *args, **kwargs)
        self.root = manager

    def create(self):
        query = Sql.get().get_active_query()
        # tables = query.get_tables()
        # attributes = query.get_attributes()

        self.root.create_frame("order_menu", self)

        # Title
        tk.Label(self, text="Order Attributes", **FONT_MEDIUM).pack(
            **{**PACK_FILL_X, **PACK_TOP}
        )

        query.update_ordering()
        for i, attribute in enumerate(query.ordering_vars.keys()):
            query.ordering_vars[attribute].set(str(i + 1))

        def form_attribute_ordering(root: tk.Frame) -> tk.Frame:
            full_attribute_list = query.get_ordered_attributes()
            options = [str(i + 1) for i in range(len(query.ordering_vars))]

            order_frame = tk.Frame(root, name="ordering")
            
            order_frame.columnconfigure(0, weight=2)
            order_frame.columnconfigure(1, weight=1)

            for i, attribute in enumerate(full_attribute_list):
                row = i % 16
                column = 2*(i // 16)
                order_frame.rowconfigure(i, weight=1)
                variable = query.ordering_vars[attribute]
                tk.Label(order_frame, text=attribute, **FONT_SMALL).grid(row=row, column=column)
                option = tk.OptionMenu(
                    order_frame,
                    variable,
                    *options,
                    command=lambda x, variable=variable, val=i + 1, frame=order_frame, func=form_attribute_ordering, root=root: [
                        [
                            var.set(str(val))
                            if var.get() == variable.get() and var != variable
                            else None
                            for var in query.ordering_vars.values()
                        ],
                        frame.destroy(),
                        func(root).pack(**PACK_FILL_Y),
                    ],
                )
                option.grid(row=row, column=column+1)
                option.config(**FONT_SMALL)

            return order_frame

        form_attribute_ordering(self).pack(**PACK_FILL_Y)

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
        attributes = Sql.get().get_active_query().get_attributes()

        Sql.get().query()

        self.root.destroy_frame("results_menu")
        results_menu = ResultsMenu(self.root)
        results_menu.create()
        self.root.pack("results_menu")

    def goto_prev(self):
        self.root.pack("conditional_menu")
