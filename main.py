import tkinter as tk
from tkinter import ttk

from constants import *
from menus.main_menu import MainMenu
from sql import Sql
from tk_manager import TkManager

ROOT = tk.Tk()

ttk.Style().configure("font_small.TCheckbutton", **FONT_SMALL)


def main():
    # Create entry menu

    ROOT.update_idletasks()
    ROOT.update()

    ROOT.update_idletasks()
    ROOT.update()

    manager = TkManager(ROOT)
    ROOT.title("Matthew Family Real Estate Portal")
    Sql.get()
    Sql.get().create_query()

    main_menu = MainMenu(manager)
    main_menu.create()
    manager.pack("main_menu")  # Default menu
    ROOT.mainloop()


if __name__ == "__main__":
    main()
