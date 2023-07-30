import tkinter as tk

from constants import *

class Tk_Manager():
    def __init__(self, root: tk.Tk):
        self.root = root
        
        self.root.geometry("1600x900+20+20")
        
        self.root.configure(bg="#FF00FF") # meant to look bad
        
        self._frames = dict()

    def create_frame(self, frame_name: str, kwargs={}) -> tk.Frame:
        if "bg" in kwargs:
            frame = tk.Frame(self.root, **kwargs)
        else:
            frame = tk.Frame(self.root, bg="#FF00FF", **kwargs)
        self._frames[frame_name] = frame
        return frame

    # def add_frame(self, frame: tk.Frame, name: str):
    #     self._frames[name] = frame
    
    def get_frame(self, frame_name: str) -> tk.Frame:
        return self._frames[frame_name]
    
    def pack(self, frame_name: str):
        frame = self.get_frame(frame_name)
        frame.pack(fill="both", expand=True)

def main():
    MANAGER = Tk_Manager(tk.Tk())
    main_menu = MANAGER.create_frame("main_menu", {"bg": "#FFEECC"})
    main_menu.configure()
    
    canvas = tk.Canvas(main_menu, bg="#FFE0CC")
    
    canvas.create_text(40, 40, text="Text 2")
    
    canvas.pack()
    
    def create_button_row(source: tk.Frame, buttons: list[tuple[str, callable]], frame_args={}, button_args={}, grid_args={}) -> tk.Frame:
        grid_frame = tk.Frame(source, **frame_args)
        
        for i, button in enumerate(buttons):
            name, callback = button
            tk.Button(grid_frame, text=name, command=callback, **button_args).grid(column=i, **grid_args)
            grid_frame.grid_columnconfigure(i, weight=1)
        
        return grid_frame
    
    def callback():
        print("pressed")
    
    grid_frame = create_button_row(
        main_menu,
        [
            ("button_0", callback),
            ("button_1", callback),
            ("button_2", callback),
            ("button_3", callback)
        ],
        frame_args={"bg": "#000000", **SMALL_PAD},
        button_args={**FONT_MEDIUM, **LEFT_ALIGN},
        grid_args={"row": 0, **FILL_X, **SMALL_PAD}
    )
    
    grid_frame.pack(fill="x", side="bottom")
    
    #tk.Label(main_menu, text="Text").pack()
    
    MANAGER.pack("main_menu")
    
    MANAGER.root.mainloop()

if __name__ == "__main__":
    main()
