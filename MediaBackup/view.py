from tkinter import *

from MediaBackup.constants import Colors
from MediaBackup.controller import Controller


class View:
    def __init__(self, master):
        controller = Controller()
        self.frame = Frame(master)
        self.frame.grid_rowconfigure(0, weight=1, minsize=100)
        self.frame.grid_columnconfigure(0, weight=1, minsize=100)
        self.frame.grid_columnconfigure(1, weight=1, minsize=100)
        self.frame.grid_columnconfigure(2, weight=1, minsize=100)
        self.frame.grid_columnconfigure(3, weight=1, minsize=100)
        self.frame.grid_columnconfigure(4, weight=1, minsize=100)
        self.frame.grid_rowconfigure(1, weight=1, minsize=100)
        self.frame.grid(row=1, columnspan=5, sticky='nesw')

        self.btn_load = Button(self.frame, text="load", bg=Colors.BUTTON_COLOR, command=lambda: controller.print())
        self.btn_load.grid(row=0, column=0, columnspan=1, sticky='nesw')

        self.btn_dest1 = Button(self.frame, text="dest1",
                                command=lambda: self.btn_load.grid_forget())
        self.btn_dest1.grid(row=0, column=1, columnspan=2, sticky='nesw')

        self.btn_dest2 = Button(self.frame, text="dest2",
                                command=lambda: self.btn_load.grid(row=0, column=0, sticky='nesw'))
        self.btn_dest2.grid(row=0, column=3, columnspan=2, sticky='nesw')

        listbox = Listbox(self.frame)
        listbox.grid(row=1, columnspan=5, sticky='nesw')
        self.frame.pack(expand=True, fill="both")
