import tkinter as tk

# import random

PRIMARY_FRAME: tk.Frame
SECONDARY_FRAME: tk.Frame

data = [
    [1, 2, 3,],
    [4, 5, 6,],
    [7, 8, 9,],
]

def main():
    window = tk.Tk()
    window.configure(bg="#FFEEDD")
    #window.wm_attributes("-transparentcolor", "#FFFFFE")
    
    def callback() -> None:
        print("Ya got me!")
        PRIMARY_FRAME.pack_forget()
        SECONDARY_FRAME.pack()
        
    def callback1() -> None:
        print("Ya didn't got me!")
        SECONDARY_FRAME.pack_forget()
        PRIMARY_FRAME.pack()
    
    window.minsize(1600, 900)
    
    PRIMARY_FRAME = tk.Frame(window)
    #primary_frame.grid()
    greeting = tk.Label(
        PRIMARY_FRAME,
        text="Mathew Family Real-estate Management System",
        font=("helvetica", 48),
        bg="#FFFFFE"
    )
    button = tk.Button(
        PRIMARY_FRAME,
        text="Mathew Family Real-estate Management System",
        font=("helvetica", 24),
        command=callback,
        bg="#FFFFFE"
    )
    greeting.pack()
    button.pack()
    
    PRIMARY_FRAME.pack(side="top")
    
    SECONDARY_FRAME = tk.Frame(window)
    #primary_frame.grid()
    greeting1 = tk.Label(
        SECONDARY_FRAME,
        text="Second",
        font=("helvetica", 48),
        bg="#FFFFFE"
    )
    button1 = tk.Button(
        SECONDARY_FRAME,
        text="Mathew Family Real-estate Management System",
        font=("helvetica", 24),
        command=callback1,
        bg="#FFFFFE"
    )
    subframe = tk.Frame(
        SECONDARY_FRAME
    )
    greeting1.pack()
    button1.pack()
    for i in range(len(data)):
        for j in range(len(data[i])):
            e = tk.Label(subframe, width=10, text=str(data[i][j]), font=("helvetica", 24))
            e.configure(background="#ffcccc")
            e.grid(row=i, column=j, sticky="w", padx=1, pady=1)

    subframe.configure(bg="#000000", padx=1, pady=1, width=300, height=250)
    subframe.pack()
    
    #e.pack()
    
    #greeting.pack()
    
    window.mainloop()

if __name__ == "__main__":
    main()
