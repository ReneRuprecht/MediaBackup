from tkinter import Toplevel, ttk, Button

from MediaBackup.settings import DbViewStyle


class DbView:
    def __init__(self, master, controller):
        self.frame = Toplevel(master)
        if controller.db_enabled:
            self.btn_load = Button(self.frame, text="Lese Datenbank",
                                   command=lambda: controller.fill_table())
            self.btn_load.grid(row=0, column=0, sticky='nesw')

        # Table
        self.table = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6), height=5, show="headings")
        if controller.db_enabled:
            self.table.grid(row=1, columnspan=13, rowspan=13, sticky='nesw')
        else:
            self.table.grid(row=0, columnspan=14, rowspan=13, sticky='nesw')
        self.table.heading(1, text="Original Pfad")
        self.table.heading(2, text="Neuer Pfad")
        self.table.heading(3, text="Dateiname")
        self.table.heading(4, text="Dateigröße")
        self.table.heading(5, text="Dateitype")
        self.table.heading(6, text="MD5")
        # self.table.heading(4, text="MD5 Hashes")

        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        if controller.db_enabled:
            self.table.grid(row=1, columnspan=13, rowspan=13, sticky='nesw')
        else:
            self.table.grid(row=0, columnspan=14, rowspan=13, sticky='nesw')
        scroll.grid(row=1, column=13, rowspan=13, stick="nesw")
        self.table.configure(yscrollcommand=scroll.set)
        # end table
        DbViewStyle(self.frame)

    def fill_table(self, db_object_array):
        # fills the table with the file informations
        for db_object in db_object_array:
            self.table.insert('', 'end',
                              values=(db_object['original_path'], db_object['new_path'], db_object['filename'],
                                      db_object['size'], db_object['type'], db_object['md5']
                                      ))
