import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as popup

from constants import *
from sql import SQL_Interface
from tk_manager import Tk_Manager

MANAGER = Tk_Manager(tk.Tk())
ACTIVE_TABLES = (
    tk.StringVar(MANAGER.root),
    tk.StringVar(MANAGER.root),
    tk.StringVar(MANAGER.root),
)
ACTIVE_ATTRIBUTES: tuple[list[tk.BooleanVar]] = (
    [],
    [],
    [],
)
SQL = SQL_Interface()
ttk.Style().configure("font_small.TCheckbutton", **FONT_SMALL)


def main():
    # Create menus
    create_main_menu()

    # Finalize window
    MANAGER.pack("main_menu")  # Default menu
    MANAGER.root.mainloop()


def create_main_menu() -> None:
    # Main menu
    main_menu = MANAGER.create_frame("main_menu", {"bg": "#B22"})

    tk.Label(main_menu, text="Select tables to query", **FONT_MEDIUM).pack(
        **{**PACK_FILL_X, **PACK_TOP}
    )

    # Main menu span
    span_frame = tk.Frame(main_menu)

    options = [
        tk.OptionMenu(span_frame, ACTIVE_TABLES[0], *["none", *SQL.tables]),
        tk.OptionMenu(span_frame, ACTIVE_TABLES[1], *["none", *SQL.tables]),
        tk.OptionMenu(span_frame, ACTIVE_TABLES[2], *["none", *SQL.tables]),
    ]

    widgets: list[tk.Widget] = [
        *options,
        tk.Label(span_frame),
        tk.Button(span_frame, text="Proceed", command=goto_table_menu, **FONT_SMALL),
    ]

    for i, option in enumerate(options):
        option.config(width=6)
        option.config(direction="above")
        option.config(**FONT_SMALL)
        ACTIVE_TABLES[i].set("none")

    for i, widget in enumerate(widgets):
        widget.grid(row=0, column=i, **GRID_FILL_BOTH)
        span_frame.grid_columnconfigure(i, weight=1)

    span_frame.pack(fill="x", side="bottom")


def create_table_menu(number_of_tables: int) -> None:
    # Remove frame if existing
    MANAGER.destroy_frame("table_menu_0")

    # Main menu
    table_menu = MANAGER.create_frame("table_menu_0", {"bg": "#2B2"})

    tk.Label(table_menu, text="Select attributes to return", **FONT_MEDIUM).pack(
        **{**PACK_FILL_X, **PACK_TOP}
    )

    tk.Button(
        table_menu, text="Proceed", command=goto_prompt_result, **FONT_MEDIUM
    ).pack(**{**PACK_FILL_X, **PACK_BOTTOM})

    lists_frame = tk.Frame(table_menu, **HIGHLIGHT_1PT_BLACK)

    for i in range(number_of_tables):
        table_name = ACTIVE_TABLES[i].get()

        active_attribute_list = ACTIVE_ATTRIBUTES[i]
        active_attribute_list.clear()

        list_frame = tk.Frame(lists_frame, bg="#CCC", **HIGHLIGHT_1PT_BLACK)

        # Create frame to contain canvas and scroll bar
        outer_frame = tk.Frame(list_frame)

        # Create and place canvas
        canvas = tk.Canvas(outer_frame, height=10000)

        # Create and bind scroll bar
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(**{**PACK_FILL_Y, **PACK_RIGHT})
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create and populate subframe
        check_boxes_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=check_boxes_frame, anchor="nw")

        # Create attribute check boxes
        for row, attribute in enumerate(SQL.table_attributes[table_name]):
            bool_var = tk.BooleanVar(MANAGER.root, value=False)
            checkbox = tk.Checkbutton(
                check_boxes_frame,
                offvalue=False,
                onvalue=True,
                variable=bool_var,
                text=attribute,
                **FONT_SMALL,
            )
            active_attribute_list.append(bool_var)

            checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

        # Enable and disable all buttons
        button_frame = tk.Frame(list_frame, **HIGHLIGHT_1PT_BLACK)
        tk.Button(
            button_frame,
            text="disable all",
            command=lambda i=i: [
                attribute.set(False) for attribute in ACTIVE_ATTRIBUTES[i]
            ],
            **FONT_SMALL,
        ).pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        tk.Button(
            button_frame,
            text="enable all",
            command=lambda i=i: [
                attribute.set(True) for attribute in ACTIVE_ATTRIBUTES[i]
            ],
            **FONT_SMALL,
        ).pack(**{**PACK_FILL_X, **PACK_BOTTOM})
        button_frame.pack(**{**PACK_BOTTOM, **PACK_FILL_X})

        # Table title
        tk.Label(
            list_frame, text=table_name, **{**FONT_MEDIUM, **HIGHLIGHT_1PT_BLACK}
        ).pack(**{**PACK_TOP, **PACK_FILL_X})

        # Check boxes
        canvas.pack(expand=True, **{**PACK_TOP, **PACK_FILL_Y})

        # pack frames
        outer_frame.pack(**PACK_FILL_Y)
        list_frame.pack(**{**PACK_FILL_Y, **PACK_LEFT})

        # Set scroll region
        canvas.update()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))

    # Fill in final gap
    # tk.Label(lists_frame, bg="#CCC").pack(**{**PACK_RIGHT, **PACK_FILL_BOTH})

    lists_frame.pack({**PACK_LEFT, **PACK_FILL_BOTH})


def goto_table_menu():
    number_of_tables = 0
    for var in ACTIVE_TABLES:
        val = var.get()
        if val == "none":
            break
        number_of_tables += 1

    if len(set([var.get() for var in ACTIVE_TABLES][:number_of_tables])) < number_of_tables:
        popup.showinfo("ERROR", "Duplicate tables not allowed!")
        return

    if number_of_tables == 0:
        popup.showinfo("ERROR", "The first table selection cannot be none!")
        return

    if number_of_tables == 2:
        table_0_attributes = SQL.table_attributes[ACTIVE_TABLES[0].get()]
        table_1_attributes = SQL.table_attributes[ACTIVE_TABLES[1].get()]

        valid01 = any(
            [attribute in table_1_attributes for attribute in table_0_attributes]
        )

        if not (valid01):
            popup.showinfo("ERROR", "Tables cannot be naturally joined!")
            return

    if number_of_tables == 3:
        table_0_attributes = SQL.table_attributes[ACTIVE_TABLES[0].get()]
        table_1_attributes = SQL.table_attributes[ACTIVE_TABLES[1].get()]
        table_2_attributes = SQL.table_attributes[ACTIVE_TABLES[2].get()]

        valid01 = any(
            [attribute in table_1_attributes for attribute in table_0_attributes]
        )
        valid12 = any(
            [attribute in table_2_attributes for attribute in table_1_attributes]
        )
        valid20 = any(
            [attribute in table_0_attributes for attribute in table_2_attributes]
        )

        if (valid01 + valid12 + valid20) < 2:
            popup.showinfo("ERROR", "Tables cannot be naturally joined!")
            return

    create_table_menu(number_of_tables)
    MANAGER.pack("table_menu_0")


def goto_prompt_result():
    number_of_tables = 0
    for var in ACTIVE_TABLES:
        val = var.get()
        if val == "none":
            break
        number_of_tables += 1

    tables = [var.get() for var in ACTIVE_TABLES][:number_of_tables]
    attributes = [
        [var.get() for var in ACTIVE_ATTRIBUTES[i]]
        for i in range(len(ACTIVE_ATTRIBUTES))
    ][:number_of_tables]

    if sum([sum(attribute_list) for attribute_list in attributes]) == 0:
        popup.showinfo("ERROR", "Query must have at least one attribute")
        return

    results = SQL.query(tables, attributes)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
