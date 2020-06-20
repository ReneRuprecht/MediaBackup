from tkinter import Frame, Label, Button
from tkinter import ttk, filedialog
from tkinter.messagebox import showerror, showinfo

from MediaBackup.constants import Colors, Texts, Buttons
from MediaBackup.settings import MainViewStyle


class MainView:

    def __init__(self, master, controller):
        self.frame = Frame(master)
        self.frame.pack(expand=True, fill="both")
        # start source related area
        self.label_source = Label(self.frame, text="Quelle", fg=Colors.TEXT_COLOR,
                                  bg=Colors.BACKGROUND_COLOR,
                                  font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_source.grid(row=1, column=1, sticky='nesw')

        self.label_source_info = Label(self.frame, text="Wähle eine Quelle aus", fg=Colors.TEXT_COLOR,
                                       bg=Colors.BACKGROUND_COLOR,
                                       font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_source_info.grid(row=2, column=1, sticky='nesw')
        # controller.select_path(self.btn_load)
        self.btn_load = Button(self.frame, text="Quelle wählen",
                               command=lambda: controller.select_path(self.btn_load))
        self.btn_load.grid(row=3, column=1, sticky='nesw')

        self.btn_start = Button(self.frame, text="Kopieren starten",
                                command=lambda: controller.start_copy())

        self.btn_start.grid(row=6, column=1, sticky='nesw')
        # end source related area

        # start copy related area
        self.label_copy = Label(self.frame, text="Kopierpfad wählen", fg=Colors.TEXT_COLOR,
                                bg=Colors.BACKGROUND_COLOR,
                                font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_copy.grid(row=1, column=5, sticky='nesw')

        self.label_copy_info = Label(self.frame, text="Wähle ein Kopier Zielverzeichnis aus", fg=Colors.TEXT_COLOR,
                                     bg=Colors.BACKGROUND_COLOR,
                                     font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_copy_info.grid(row=2, column=5, sticky='nesw')

        self.btn_copy = Button(self.frame, text="Kopierpfad wählen", width=Buttons.DEST_SIZE,
                               command=lambda: controller.select_path(self.btn_copy))
        self.btn_copy.grid(row=3, column=5)

        self.label_copy_path = Label(self.frame, fg=Colors.TEXT_COLOR,
                                     bg=Colors.BACKGROUND_COLOR,
                                     font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_copy_path.grid(row=6, column=5, sticky='nesw')

        self.progressbar_copy = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                orient="horizontal",
                                                mode="determinate", maximum=100, value=20)

        # end copy related area

        # start backup related area
        self.label_backup = Label(self.frame, text="Backuppfad wählen", fg=Colors.TEXT_COLOR,
                                  bg=Colors.BACKGROUND_COLOR,
                                  font=(Texts.HEADER_FONT, Texts.HEADER_SIZE))
        self.label_backup.grid(row=1, column=10, sticky='nesw')

        self.label_backup_info = Label(self.frame, text="Wähle ein Backup Zielverzeichnis aus", fg=Colors.TEXT_COLOR,
                                       bg=Colors.BACKGROUND_COLOR,
                                       font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_backup_info.grid(row=2, column=10, sticky='nesw')

        self.btn_backup = Button(self.frame, text="Backuppfad wählen", width=Buttons.DEST_SIZE,
                                 command=lambda: controller.select_path(self.btn_backup))
        self.btn_backup.grid(row=3, column=10)

        self.label_backup_path = Label(self.frame, fg=Colors.TEXT_COLOR,
                                       bg=Colors.BACKGROUND_COLOR,
                                       font=(Texts.INFO_FONT, Texts.INFO_SIZE))
        self.label_backup_path.grid(row=6, column=10, sticky='nesw')

        # Progressbar2
        self.progressbar_backup = ttk.Progressbar(self.frame, style="blue.Horizontal.TProgressbar",
                                                  orient="horizontal",
                                                  mode="determinate", maximum=100, value=20)
        # end backup related area

        # Table
        self.table = ttk.Treeview(self.frame, columns=(1, 2, 3, 4), height=5, show="headings")
        self.table.grid(row=8, columnspan=13, rowspan=12, sticky='nesw')
        self.table.heading(1, text="Dateifpad")
        self.table.heading(2, text="Dateiname")
        self.table.heading(3, text="Dateigröße")
        self.table.heading(4, text="DateiType")
        # self.table.heading(4, text="MD5 Hashes")

        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.table.yview)
        scroll.grid(row=8, column=13, rowspan=12, stick="nesw")
        self.table.configure(yscrollcommand=scroll.set)
        # end table
        MainViewStyle(self.frame)

        self.btn_db = Button(self.frame, text="db", width=1,
                             command=lambda: controller.open_db_view())
        self.btn_db.grid(row=0, column=13)

    # progressbar_copy
    def show_progressbar_copy(self):
        self.progressbar_copy.grid(row=2, column=5, rowspan=4, sticky='nesw')

    def hide_progressbar_copy(self):
        self.progressbar_copy.grid_forget()

    # end progressbar_copy

    # progressbar_backup
    def show_progressbar_backup(self):
        self.progressbar_backup.grid(row=2, column=10, rowspan=4, sticky='nesw')

    def hide_progressbar_backup(self):
        self.progressbar_backup.grid_forget()

    # end progressbar_backup

    @staticmethod
    def update_progressbar(proressbar, value):
        # updates the progressbar value
        if value < 0:
            value = 0

        proressbar["value"] = value

    def fill_table(self, object_array):
        # fills the table with the file informations
        for i in object_array:
            self.table.insert('', 'end',
                              values=(
                                  i.get_file_path(), i.get_file_name(), i.get_file_size_with_ident(),
                                  i.get_file_type()))

    @staticmethod
    def show_messagebox(style, header, text):
        # shows a messagebox depending on the style
        if style == "Error":
            showerror(header, text)
        elif style == "Info":
            showinfo(header, text)

    @staticmethod
    def get_folder_path():
        # shows the folderdialog and returns the selected folder
        folder_name = filedialog.askdirectory()
        return folder_name

    @staticmethod
    def set_label_text(label_object, text):
        # sets a label text of the label_object
        label_object['text'] = text

    @staticmethod
    def change_progressbar_style(progressbar, color):
        # sets the progressbar color
        if color.lower() == "blue":
            progressbar['style'] = "blue.Horizontal.TProgressbar"
        elif color.lower() == "yellow":
            progressbar['style'] = "yellow.Horizontal.TProgressbar"
        elif color.lower() == "green":
            progressbar['style'] = "green.Horizontal.TProgressbar"
        elif color.lower() == "red":
            progressbar['style'] = "red.Horizontal.TProgressbar"

    def reset_form(self):
        # resets the gui elements and its values
        self.set_label_text(self.label_copy, "Kopierpfad wählen")
        self.set_label_text(self.label_copy_path, "")
        self.hide_progressbar_copy()
        self.set_label_text(self.label_backup, "Backuppfad wählen")
        self.set_label_text(self.label_backup_path, "")
        self.hide_progressbar_backup()
