from tkinter import ttk


class Settings:
    def __init__(self, frame):
        self.set_style()
        self.set_frame_grid_layout(frame)

    @staticmethod
    def set_style():
        ttk_style = ttk.Style()
        ttk_style.theme_use('clam')
        ttk_style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        ttk_style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
        ttk_style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

    @staticmethod
    def set_frame_grid_layout(frame):
        frame.grid_rowconfigure(0, weight=1, minsize=100)
        frame.grid_columnconfigure(0, weight=1, minsize=100)
        frame.grid_columnconfigure(1, weight=1, minsize=100)
        frame.grid_columnconfigure(2, weight=1, minsize=100)
        frame.grid_columnconfigure(3, weight=1, minsize=100)
        frame.grid_columnconfigure(4, weight=1, minsize=100)
        frame.grid_rowconfigure(1, weight=1, minsize=100)
        frame.grid(row=1, columnspan=5, sticky='nesw')
