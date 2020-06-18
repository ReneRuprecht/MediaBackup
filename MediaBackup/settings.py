from tkinter import ttk

from MediaBackup.constants import Colors


class Settings:
    def __init__(self, frame):
        self.set_style()
        self.set_frame_grid_layout(frame)
        frame.configure(bg=Colors.BACKGROUND_COLOR)

    @staticmethod
    def set_style():
        ttk_style = ttk.Style()
        ttk_style.theme_use('clam')
        ttk_style.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        ttk_style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
        ttk_style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')

    @staticmethod
    def set_frame_grid_layout(frame):
        for i in range(20):
            # table rows
            if i >= 8:
                frame.grid_rowconfigure(i, minsize=20, weight=1)
            # other rows
            else:
                frame.grid_rowconfigure(i, minsize=20)

        for i in range(13):
            # spacer columns
            if i == 0 or i == 3 or i == 8:
                frame.grid_columnconfigure(i, minsize=20)

            # dest1 and dest2 columns
            if i == 5 or i == 10:
                frame.grid_columnconfigure(i, weight=2)
