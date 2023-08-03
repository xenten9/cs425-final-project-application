import tkinter as tk
import tkinter.messagebox as popup

from constants import *
from menus.conditional_menu import ConditionalMenu
from query import Query
from sql import Sql
from tk_manager import TkManager


class AttributeMenu(tk.Frame):
    def __init__(self, root: TkManager, *args, **kwargs) -> None:
        super().__init__(root.root, *args, **kwargs)
        self.root = root

    def create(self, query: Query):
        tables = query.get_tables()
        
        self.root.create_frame("attribute_menu", self)

        # Title
        tk.Label(self, text="Select attributes to return", **FONT_MEDIUM).pack(
            **{**PACK_FILL_X, **PACK_TOP}
        )

        # Bottom menu buttons
        frame = tk.Frame(self, bg="yellow")
        frame.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        frame.columnconfigure(0, weight=1)
        tk.Button(
            frame,
            text="Go back",
            command=lambda query=query: self.goto_prev(query),
            **FONT_MEDIUM,
        ).grid(row=0, column=0, **GRID_FILL_X)
        frame.columnconfigure(1, weight=1)
        tk.Button(
            frame,
            text="Proceed",
            command=lambda query=query: self.goto_next(query),
            **FONT_MEDIUM,
        ).grid(row=0, column=1, **GRID_FILL_X)

        # Lists frame
        canvas = tk.Canvas(self, bg="green")
        canvas.pack(expand=True, **PACK_FILL_BOTH)
        canvas_frame = tk.Frame(canvas, bg="red", **HIGHLIGHT_1PT_BLACK)
        canvas.create_window(0, 0, window=canvas_frame, anchor="nw", width=50000)
        canvas.bind(
            "<Configure>",
            lambda e, frame=canvas_frame: frame.config(height=e.height),
        )
        canvas_frame.pack_propagate(0)  # This is so unbeleivably crucial

        # Create and bind scroll bar
        scrollbar = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        scrollbar.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        canvas.configure(xscrollcommand=scrollbar.set)

        query.update_attributes()

        for table in tables:
            list_frame = tk.Frame(canvas_frame, bg=f"#00F")

            list_frame.pack(**{**PACK_LEFT, **PACK_FILL_Y})

            # Control all buttons
            buttons_frame = tk.Frame(list_frame)
            tk.Button(
                buttons_frame,
                text="disable all",
                command=lambda table=table: [
                    attribute.set(False)
                    for attribute in query.attribute_vars[table].values()
                ],
                **FONT_SMALL,
            ).pack(**{**PACK_FILL_X, **PACK_BOTTOM})
            tk.Button(
                buttons_frame,
                text="enable all",
                command=lambda table=table: [
                    attribute.set(True)
                    for attribute in query.attribute_vars[table].values()
                ],
                **FONT_SMALL,
            ).pack(**{**PACK_FILL_X, **PACK_BOTTOM})
            buttons_frame.pack(**{**PACK_BOTTOM, **PACK_FILL_X})

            # Check box domain
            check_frame = tk.Frame(list_frame)
            check_frame.pack(expand=True, **{**PACK_TOP, **PACK_FILL_BOTH})

            check_canvas = tk.Canvas(check_frame, height=10000)
            check_canvas.pack(expand=True, **PACK_FILL_BOTH)
            check_canvas_frame = tk.Frame(canvas, **HIGHLIGHT_1PT_BLACK)
            check_canvas.create_window(0, 0, window=check_canvas_frame, anchor="nw")
            check_canvas.bind(
                "<Configure>",
                lambda e, frame=check_canvas_frame: frame.config(
                    width=e.width, height=e.height
                ),
            )
            check_canvas_frame.pack_propagate(0)  # This is so unbeleivably crucial

            check_subframe = tk.Frame(check_canvas_frame, width=400)
            check_subframe.pack(**{**PACK_FILL_BOTH})

            check_subframe.columnconfigure(0, weight=1)

            for row, attribute in enumerate(Sql.get().table_attributes[table]):
                bool_var = query.attribute_vars[table][attribute]
                checkbox = tk.Checkbutton(
                    check_subframe,
                    variable=bool_var,
                    text=attribute,
                    **FONT_SMALL,
                )
                check_subframe.rowconfigure(row, weight=1)
                checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

        # Update horizontal scroll region
        canvas.config(
            scrollregion=(
                0,
                0,
                385 * len(tables),
                0,
            )
        )

    def goto_next(self, query: Query):
        root = self.root
        attributes = query.get_attributes()

        # Select at least one attribute
        if (
            sum([len(attribute_list) for attribute_list in attributes.values()])
            == 0
        ):
            popup.showinfo("ERROR", "Query must have at least one attribute")
            return

        # Make room for new conditional menu
        root.destroy_frame("conditional_creator")
        conditional_creator = ConditionalMenu(root, query)
        conditional_creator.create()
        root.pack("conditional_creator")

    def goto_prev(self, query: Query):
        pass