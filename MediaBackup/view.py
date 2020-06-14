from tkinter import *
from tkinter import ttk

from MediaBackup.constants import Colors
from MediaBackup.settings import Settings


class View:
    def __init__(self, master):
        self.frame = Frame(master)
        Settings(self.frame)

        # Button Quelle
        self.btn_load = Button(self.frame, text="load", bg=Colors.BUTTON_COLOR,
                               command=lambda: self.toggle_both_progressbars_visibility())
        self.btn_load.grid(row=0, column=0, columnspan=1, sticky='nesw')

        # Button Zielverzeichnis 1
        self.btn_dest1 = Button(self.frame, text="dest1",
                                command=lambda: "")
        self.btn_dest1.grid(row=0, column=1, columnspan=2, sticky='nesw')

        # Progressbar1
        self.progressbar_dest1 = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                 orient="horizontal",
                                                 mode="determinate", maximum=100, value=20)

        # Button Zielverzeichnis 2
        self.btn_dest2 = Button(self.frame, text="dest2",
                                command=lambda: self.show_btn_dest1())
        self.btn_dest2.grid(row=0, column=3, columnspan=2, sticky='nesw')

        # Progressbar2
        self.progressbar_dest2 = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                 orient="horizontal",
                                                 mode="determinate", maximum=100, value=20)

        # Listbox für die geladenen Dateien
        listbox = Listbox(self.frame)
        listbox.grid(row=1, columnspan=5, sticky='nesw')

        self.frame.pack(expand=True, fill="both")

    # btn_dest1
    def show_btn_dest1(self):
        self.btn_dest1.grid(row=0, column=1, columnspan=2, sticky='nesw')

    def hide_btn_dest1(self):
        self.btn_dest1.grid_forget()

    # progressbar_dest1
    def show_progressbar_dest1(self):
        self.progressbar_dest1.grid(row=0, column=1, columnspan=2, sticky='nesw')

    def hide_progressbar_dest1(self):
        self.progressbar_dest1.grid_forget()

    # btn_dest2
    def show_btn_dest2(self):
        self.btn_dest2.grid(row=0, column=1, columnspan=2, sticky='nesw')

    def hide_btn_dest2(self):
        self.btn_dest2.grid_forget()

    # progressbar_dest1
    def show_progressbar_dest2(self):
        self.progressbar_dest2.grid(row=0, column=3, columnspan=2, sticky='nesw')

    def hide_progressbar_dest2(self):
        self.progressbar_dest2.grid_forget()

    def toggle_both_progressbars_visibility(self):
        if self.progressbar_dest1.winfo_ismapped() and self.progressbar_dest2.winfo_ismapped():
            self.hide_progressbar_dest1()
            self.hide_progressbar_dest2()
        else:
            self.show_progressbar_dest1()
            self.show_progressbar_dest2()
