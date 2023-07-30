import tkinter as tk

from constants import *
from helper_elements import create_button_row
from tk_manager import Tk_Manager


def main():
    # Create window
    MANAGER = Tk_Manager(tk.Tk())

    # Main menu
    main_menu = MANAGER.create_frame("main_menu", {"bg": "#B22"})
    main_menu.configure()

    def callback():  # TODO replace with useful callbacks
        print("pressed")

    grid_frame = create_button_row(
        main_menu,
        [
            ("button_0", callback),
            ("button_1", callback),
            ("button_2", callback),
            ("button_3", callback),
        ],
        frame_args={"bg": "#000000", **SMALL_PAD},
        button_args={**FONT_MEDIUM, **LEFT_ALIGN},
        grid_args={**FILL_X, **SMALL_PAD},
    )
    grid_frame.pack(fill="x", side="bottom")

    # Finalize window
    MANAGER.pack("main_menu")  # Default menu
    MANAGER.root.mainloop()


if __name__ == "__main__":
    main()
