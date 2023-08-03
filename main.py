from datetime import date
from decimal import Decimal
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as popup
import numpy as np

from constants import *
from menus.attribute_menu import AttributeMenu
from query import Query
from sql import Sql
from tk_manager import TkManager

MANAGER = TkManager(tk.Tk())

CONDITIONALS: list[
    tuple[
        tk.StringVar,  # Operand 1 (table_name or custom)
        tk.StringVar,  # Operator
        tk.StringVar,  # Operand 2 (table_name or custom)
        tk.StringVar,  # Operand 2 optional custom
        tk.StringVar,  # Logical Join
    ]
] = []
SQL = Sql.get()

QUERY = Query()
ttk.Style().configure("font_small.TCheckbutton", **FONT_SMALL)

def main():
    # Create menus
    create_main_menu()

    # Finalize window
    MANAGER.pack("main_menu")  # Default menu
    MANAGER.root.mainloop()


# Create menus
def create_main_menu() -> None:
    # Main menu
    main_menu = MANAGER.create_frame("main_menu", kwargs={"bg": "#B22"})

    # Title
    tk.Label(main_menu, text="Select tables to query", **FONT_MEDIUM).pack(
        **{**PACK_FILL_X, **PACK_TOP}
    )

    # Accursed mess that is another checkbox grid
    check_boxes_frame = tk.Frame(main_menu, padx=20, pady=20)

    for row, table in enumerate(SQL.tables):
        bool_var = QUERY.table_vars[table]
        checkbox = tk.Checkbutton(
            check_boxes_frame,
            variable=bool_var,
            text=table,
            **FONT_SMALL,
        )
        checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

    # Use natural joins?
    bool_var = QUERY.use_natural_join
    checkbox = tk.Checkbutton(
        check_boxes_frame,
        variable=bool_var,
        text="Use natural join?",
        **FONT_SMALL,
    )
    checkbox.grid(row=row, column=0, **GRID_ALIGN_LEFT)

    # Main menu span
    span_frame = tk.Frame(main_menu)
    widgets: list[tk.Widget] = [
        tk.Button(
            span_frame,
            text="Reset selection",
            command=lambda: [var.set(0) for var in QUERY.table_vars.values()],
            **FONT_SMALL,
        ),
        tk.Button(span_frame, text="Proceed", command=goto_table_menu, **FONT_SMALL),
    ]

    for i, widget in enumerate(widgets):
        widget.grid(row=0, column=i, **GRID_FILL_BOTH)
        span_frame.grid_columnconfigure(i, weight=1)

    # Pack frames
    span_frame.pack(**{**PACK_FILL_X, **PACK_BOTTOM})
    check_boxes_frame.pack(**{**PACK_TOP, **PACK_FILL_BOTH})


def create_attribute_menu(tables: list[str]) -> None:
    # Attribute menu
    menu = AttributeMenu(MANAGER, **{"bg": "#00F"})
    menu.create(QUERY)
    MANAGER.pack("attribute_menu")




def create_results_menu(results, headers: list[str]) -> None:
    frame_results = MANAGER.create_frame("results")

    # External UI
    tk.Label(frame_results, text="Results", **FONT_MEDIUM).pack(
        **{**PACK_TOP, **PACK_FILL_X}
    )

    tk.Button(
        frame_results,
        text="Go back to conditional",
        command=lambda: MANAGER.pack("conditional_creator"),
        **FONT_MEDIUM,
    ).pack(**{**PACK_BOTTOM, **PACK_FILL_X})

    # Table for results
    frame_table_container = tk.Frame(frame_results, bg="#228")
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

    tk.Label(frame_table, text="result #", **FONT_SMALL).grid(
        row=0, column=0, **{**SMALL_PAD, **GRID_FILL_X}
    )

    for i, header in enumerate(headers):
        tk.Label(frame_table, text=header, **FONT_SMALL_BOLD).grid(
            row=0, column=i + 1, **{**SMALL_PAD, **GRID_FILL_X}
        )

    for i, result in enumerate(results):
        tk.Label(frame_table, text=str(i + 1), **{**FONT_SMALL, **RIGHT_ALIGN}).grid(
            row=i + 1, column=0, **{**SMALL_PAD, **GRID_FILL_X}
        )
        for j, cell in enumerate(result):
            if isinstance(cell, date):
                cell = f"{cell.month}/{cell.day}/{cell.year}"
            elif isinstance(cell, Decimal):
                cell = float(cell)
                cell = "{:,.2f}".format(cell)
            tk.Label(frame_table, text=str(cell), **{**FONT_SMALL, **LEFT_ALIGN}).grid(
                row=i + 1, column=j + 1, **{**SMALL_PAD, **GRID_FILL_X}
            )

    # Packing events
    canvas.pack(expand=True, **{**PACK_TOP, **PACK_FILL_BOTH})
    frame_table_container.pack(**PACK_FILL_BOTH)

    # Set scroll region
    canvas.update()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))


# Goto menus
def goto_table_menu():
    tables = QUERY.get_tables()

    #
    if len(tables) == 0:
        popup.showinfo("ERROR", "Must select at least one table!")
        return

    # Validate table connections for Natural Join
    if QUERY.use_natural_join.get():
        # Form relation matrix
        mat: list[list[bool]] = []
        for i, table_0 in enumerate(tables):
            mat.append([])
            for table_1 in tables:
                mat[i].append(
                    any(
                        (
                            attribute in SQL.table_attributes[table_0]
                            for attribute in SQL.table_attributes[table_1]
                        )
                    )
                )

        # Check to see if all cells are accessible in n-1 (max required) steps
        if np.prod(np.mat(mat) ** (len(tables) - 1)) == 0:
            popup.showinfo("ERROR", "Tables cannot be natrual joined!")
            return

    MANAGER.destroy_frame("attribute_menu")
    create_attribute_menu(tables)
    MANAGER.pack("attribute_menu")


def goto_conditional_creator():
    tables = [table if ACTIVE_TABLES[table].get() else None for table in ACTIVE_TABLES]
    tables = list(filter(lambda x: x, tables))

    attributes = {
        table: [
            var.get()
            for var in ACTIVE_ATTRIBUTES[table].values()
        ]
        for table in tables
    }

    if sum([sum(attribute_list) for attribute_list in attributes]) == 0:
        popup.showinfo("ERROR", "Query must have at least one attribute")
        return

    MANAGER.destroy_frame("conditional_creator")
    create_conditional_menu(number_of_tables)
    MANAGER.pack("conditional_creator")


def goto_order_attributes():
    # Get number of tables
    number_of_tables = 0
    for var in ACTIVE_TABLES:
        val = var.get()
        if val == "none":
            break
        number_of_tables += 1

    # Get list of table names
    tables = [var.get() for var in ACTIVE_TABLES][:number_of_tables]

    # Get list of attributes
    attributes = [
        [var.get() for var in ACTIVE_ATTRIBUTES[i]]
        for i in range(len(ACTIVE_ATTRIBUTES))
    ][:number_of_tables]

    # Get list of unique attribute names
    ordered_attributes: list[str] = []
    for i, table in enumerate(tables):
        for j in range(len(attributes[i])):
            if attributes[i][j]:
                ordered_attributes.append(SQL.table_attributes[table][j])
    ordered_attributes = list(set(ordered_attributes))


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
    conditionals = [[var.get() for var in row] for row in CONDITIONALS]

    if sum([sum(attribute_list) for attribute_list in attributes]) == 0:
        popup.showinfo("ERROR", "Query must have at least one attribute")
        return

    results, headers = SQL.query(tables, attributes, conditionals)

    MANAGER.destroy_frame("results")
    create_results_menu(results, headers)
    MANAGER.pack("results")


if __name__ == "__main__":
    main()
