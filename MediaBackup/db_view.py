from tkinter import Toplevel, ttk, Button
from tkinter.messagebox import showerror, showinfo

from MediaBackup.settings import DbViewStyle


class DbView:
    def __init__(self, master, controller):
        self.frame = Toplevel(master)
        self.btn_load = Button(self.frame, text="Lese Datenbank",
                               command=lambda: controller.fill_table())
        self.btn_load.grid(row=0, column=0, sticky='nesw')

        # Table
        self.table = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
        self.table.grid(row=1, columnspan=13, rowspan=13, sticky='nesw')

        self.table.heading(1, text="Original Pfad")
        self.table.heading(2, text="Neuer Pfad")
        self.table.heading(3, text="Dateiname")
        self.table.heading(4, text="Dateigröße")
        self.table.heading(5, text="Dateitype")
        self.table.heading(6, text="MD5")

        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        self.table.grid(row=1, columnspan=13, rowspan=13, sticky='nesw')
        scroll.grid(row=1, column=13, rowspan=13, stick="nesw")
        self.table.configure(yscrollcommand=scroll.set)
        # end table
        DbViewStyle(self.frame)

    def fill_table(self, db_object_array):
        # fills the table with the file informations
        self.table.delete(*self.table.get_children())
        for db_object in db_object_array:
            db_object_dict = db_object.get_object_dict()
            self.table.insert('', 'end',
                              values=(
                                  db_object_dict['original_path'], db_object_dict['new_path'],
                                  db_object_dict['filename'], db_object_dict['size'],
                                  db_object_dict['type'], db_object_dict['md5']
                              ))

    @staticmethod
    def show_messagebox(style, header, text):
        # shows a messagebox depending on the style
        if style == "Error":
            showerror(header, text)
        elif style == "Info":
            showinfo(header, text)
