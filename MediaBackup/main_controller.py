import os

from .file_model import FileModel
from .main_view import View


class Controller:
    def __init__(self, master):
        self.view = View(master, self)
        self.master = master
        self.dest1_path = ""
        self.dest2_path = ""

    def start_copy(self):
        if self.dest1_path == "":
            self.view.show_error("Pfad fehlt", "Wählen Sie einen Ziel-Pfad aus")
            return
        files_array = []
        table_selection = self.view.table.selection()
        for i in table_selection:
            selected_path = self.get_path_from_table(i)
            files_array.append(selected_path)
        print(files_array)
        self.view.toggle_dest1_area()
        self.view.toggle_dest2_area()

    def get_path_from_table(self, table_item):
        return self.view.table.item(table_item)['values'][0]

    def select_path(self, dest_button):
        if dest_button['text'] == "dest1":
            self.dest1_path = self.view.get_folder_path()
            self.set_label_text(self.view.label_dest1_path, self.dest1_path)
        elif dest_button['text'] == "dest2":
            self.dest2_path = self.view.get_folder_path()
            self.set_label_text(self.view.label_dest2_path, self.dest2_path)
        elif dest_button['text'] == "load":
            src_path = self.view.get_folder_path()
            file_objects_array = self.get_all_files_from_folder(src_path)
            self.view.fill_table(file_objects_array)
        else:
            self.view.show_error("Error ausgelöst von select_path function", "Es wurde ein falscher Button übergeben")

    def set_label_text(self, label_object, text):
        self.view.set_label_text(label_object, text)

    @staticmethod
    def get_all_files_from_folder(path):
        files_array = []
        for root, dirs, files in os.walk(path):
            for file in files:
                full_file = FileModel(os.path.join(root, file))
                files_array.append(full_file)
        return files_array

    def get_dest2_is_set(self):
        if not self.dest2_path == "":
            return True
