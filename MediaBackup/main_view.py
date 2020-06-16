from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror

from MediaBackup.constants import Colors, Texts
from MediaBackup.settings import Settings


class View:
    def __init__(self, master, controller):
        self.frame = Frame(master)

        # Button Quelle

        # start source related area
        self.label_source = Label(self.frame, text="Quelle", fg=Colors.TEXT_COLOR,
                                  bg=Colors.BACKGROUND_COLOR,
                                  font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_source.grid(row=1, column=1, sticky='nesw')

        self.label_source_info = Label(self.frame, text="Wähle eine Quelle aus", fg=Colors.TEXT_COLOR,
                                       bg=Colors.BACKGROUND_COLOR,
                                       font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_source_info.grid(row=2, column=1, sticky='nesw')

        self.btn_load = Button(self.frame, text="load",
                               command=lambda: controller.load_items_to_table())
        self.btn_load.grid(row=3, column=1, sticky='nesw')

        self.btn_start = Button(self.frame, text="start",
                                command=lambda: controller.start_copy())

        self.btn_start.grid(row=6, column=1, sticky='nesw')
        # end source related area

        # start dest1 related area
        self.label_dest1 = Label(self.frame, text="Kopieren", fg=Colors.TEXT_COLOR,
                                 bg=Colors.BACKGROUND_COLOR,
                                 font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_dest1.grid(row=1, column=5, sticky='nesw')

        self.label_dest1_info = Label(self.frame, text="Wähle ein Zielverzeichnis aus", fg=Colors.TEXT_COLOR,
                                      bg=Colors.BACKGROUND_COLOR,
                                      font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_dest1_info.grid(row=2, column=5, sticky='nesw')

        self.btn_dest1 = Button(self.frame, text="dest1",
                                command=lambda: "")
        self.btn_dest1.grid(row=3, column=5, sticky='nesw')

        # Progressbar1
        self.progressbar_dest1 = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                 orient="horizontal",
                                                 mode="determinate", maximum=100, value=20)

        # end dest1 related area

        # start dest2 related area
        self.label_dest2 = Label(self.frame, text="Backup", fg=Colors.TEXT_COLOR, bg=Colors.BACKGROUND_COLOR,
                                 font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_dest2.grid(row=1, column=10, sticky='nesw')

        self.label_dest2_info = Label(self.frame, text="Wähle ein Backup Zielverzeichnis aus", fg=Colors.TEXT_COLOR,
                                      bg=Colors.BACKGROUND_COLOR,
                                      font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_dest2_info.grid(row=2, column=10, sticky='nesw')

        self.btn_dest2 = Button(self.frame, text="dest2",
                                command=lambda: "")
        self.btn_dest2.grid(row=3, column=10, sticky='nesw')

        # Progressbar2
        self.progressbar_dest2 = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                 orient="horizontal",
                                                 mode="determinate", maximum=100, value=20)
        # end dest2 related area

        # Table
        self.table = ttk.Treeview(self.frame, columns=(1, 2, 3, 4), height=5, show="headings")
        self.table.grid(row=8, columnspan=13, rowspan=12, sticky='nesw')
        self.table.heading(1, text="Dateifpad")
        self.table.heading(2, text="Dateiname")
        self.table.heading(3, text="Dateigröße")
        self.table.heading(4, text="Hash")

        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        scroll.grid(row=11, column=13, rowspan=12, stick="nesw")
        self.table.configure(yscrollcommand=scroll.set)

        Settings(self.frame)

        self.frame.pack(expand=True, fill="both")

    # start dest1 area
    def show_dest1_area(self):
        self.label_dest1.grid(row=1, column=5, sticky='nesw')
        self.label_dest1_info.grid(row=2, column=5, sticky='nesw')
        self.btn_dest1.grid(row=3, column=5, sticky='nesw')

    def hide_dest1_area(self):
        self.label_dest1.grid_forget()
        self.label_dest1_info.grid_forget()
        self.btn_dest1.grid_forget()

    # progressbar_dest1
    def show_progressbar_dest1(self):
        self.progressbar_dest1.grid(row=2, column=4, columnspan=3, rowspan=6, sticky='nesw')

    def hide_progressbar_dest1(self):
        self.progressbar_dest1.grid_forget()

    def toggle_dest1_area(self):
        if self.progressbar_dest1.winfo_ismapped():
            self.hide_progressbar_dest1()
            self.show_dest1_area()
        else:
            self.show_progressbar_dest1()
            self.hide_dest1_area()

    def change_dest1_header_text(self, text):
        self.label_dest1.text = text

    # end dest1 area

    # start dest2 area
    def show_dest2_area(self):
        self.label_dest2.grid(row=1, column=10, sticky='nesw')
        self.label_dest2_info.grid(row=2, column=10, sticky='nesw')
        self.btn_dest2.grid(row=3, column=10, sticky='nesw')

    def hide_dest2_area(self):
        self.label_dest2.grid_forget()
        self.label_dest2_info.grid_forget()
        self.btn_dest2.grid_forget()

    # progressbar_dest2
    def show_progressbar_dest2(self):
        self.progressbar_dest2.grid(row=2, column=9, columnspan=3, rowspan=6, sticky='nesw')

    def hide_progressbar_dest2(self):
        self.progressbar_dest2.grid_forget()

    def toggle_dest2_area(self):
        if self.progressbar_dest2.winfo_ismapped():
            self.hide_progressbar_dest2()
            self.show_dest2_area()
        else:
            self.show_progressbar_dest2()
            self.hide_dest2_area()

    def change_dest2_header_text(self, text):
        self.label_dest2.text = text

    # end dest2 area

    @staticmethod
    def update_progressbar(proressbar, value):
        if value < 0:
            value = 0

        proressbar["value"] = value

    def test_me(self):
        file_array = [["C:/test/1.txt"], ["C:/test/1_1.txt"]]

        for i in range(2):
            self.table.insert('', 'end', values=(file_array[i][0], i))

    @staticmethod
    def get_item_in_table():
        file_array = ["C:/test/1.txt", "C:/test/1_1.txt"]

    def fill_table(self, object_array):
        for i in object_array:
            print(i.get_file_path())
            self.table.insert('', 'end',
                              values=(i.get_file_path(), i.get_file_name(), i.get_file_size(), i.get_file_md5()))

    @staticmethod
    def showerror(header, text):
        showerror(header, text)
