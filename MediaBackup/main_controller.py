from .file_model import FileModel
from .main_view import View


class Controller:
    def __init__(self, master):
        self.view = View(master, self)
        self.master = master
        file_array = []
        self.dest1_path = ""
        self.dest2_path = ""

    def start_copy(self):
        if self.dest1_path == "":
            self.view.showerror("Error", "Kein Pfad ausgewählt")

    def load_items_to_table(self):
        array = [FileModel("C:/test/1.txt"), FileModel("C:/test/1_1.txt")]
        self.view.fill_table(array)
