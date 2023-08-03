import tkinter as tk


class TkManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("1600x900+20+20")
        self.root.configure(bg="#F0F")  # meant to look bad
        self._frames: dict[str, tk.Frame] = dict()
        self._current_frame: tk.Frame = None

    def create_frame(self, frame_name: str, frame: tk.Frame=None, kwargs={}) -> tk.Frame:
        if frame:
            self._frames[frame_name] = frame
        else:
            if "bg" not in kwargs:
                kwargs = {"bg": "#FF00FF", **kwargs}
            frame = tk.Frame(self.root, **kwargs)
            self._frames[frame_name] = frame
        return frame

    def get_frame(self, frame_name: str) -> tk.Frame:
        return self._frames[frame_name]

    def destroy_frame(self, frame_name: str) -> None:
        if self._current_frame == frame_name:
            raise ValueError(f"Can not destroy active frame <{frame_name}>.")
        if frame_name in self._frames:
            del self._frames[frame_name]

    def pack(self, frame_name: str):
        if self._current_frame:  # Unpack active frame
            self._current_frame.pack_forget()

        # Pack new frame
        frame = self.get_frame(frame_name)
        frame.pack(fill="both", expand=True)
        self._current_frame = frame
