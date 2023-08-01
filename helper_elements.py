import tkinter as tk


def create_span_row(
    frame: tk.Frame,
    widgets: list[tk.Widget],
    grid_args={},
) -> None:
    for i, widget in enumerate(widgets):
        widget.grid(row=0, column=i, **grid_args)
        #frame.grid_columnconfigure(i, weight=1)

# def create_button_row(
#     source: tk.Frame,
#     buttons: list[tuple[str, callable]],
#     frame_args={},
#     button_args={},
#     grid_args={},
# ) -> tk.Frame:

#     create_span_row()

#     for i, button in enumerate(buttons):
#         name, callback = button
#         new_button = tk.Button(grid_frame, text=name, command=callback, **button_args)
#         new_button.grid(row=0, column=i, **grid_args)
#         grid_frame.grid_columnconfigure(i, weight=1)

#     return grid_frame
