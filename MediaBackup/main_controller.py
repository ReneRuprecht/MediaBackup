import os
import shutil
import threading

from .db_controller import DbController
from .file_model import FileModel
from .main_view import MainView


class MainController:
    def __init__(self, master, db_enabled=False, db=None):
        self.view = MainView(master, self)
        self.db_view = None
        self.master = master
        # check if db is enabled and a db object was created
        self.db = None
        self.db_enabled = db_enabled
        if db_enabled and db is not None:
            self.db_enabled = db_enabled
            self.db = db
        # contains just the root section of the loaded directory
        self.root_path = ""
        self.copy_path = ""
        self.backup_path = ""
        # will contain the thread object
        self.copy_to_dests_thread = None
        # contains if a thread is running, to prevent double execution
        self.thread_running = False

    def start_copy(self):
        # check if thread is already running to prevent double execution
        if not self.thread_running:
            if self.copy_path == "":
                self.view.show_messagebox("Error", "Pfad fehlt", "Wählen Sie einen Ziel-Pfad aus")
                return
            elif self.root_path == "":
                self.view.show_messagebox("Error", "Pfad fehlt", "Wählen Sie einen Quell-Pfad aus")
                return
            elif self.root_path == self.copy_path:
                self.view.show_messagebox("Error", "Falscher Pfad",
                                          "Wählen Sie einen anderen Kopierpfad")
                return
            elif self.copy_path == self.backup_path:
                self.view.show_messagebox("Error", "Falscher Pfad",
                                          "Wählen Sie einen anderen Backuppfad")
                return
            elif len(self.view.table.selection()) <= 0:
                # checks if the user selected one or multiple items from the table
                self.view.show_messagebox("Error", "Kein Element ausgewählt",
                                          "Wählen Sie ein Element aus der Tabelle aus")
                return

            # starts the thread
            self.copy_to_dests_thread = threading.Thread(target=self.copy_procedure, args=())
            self.copy_to_dests_thread.start()
            self.thread_running = True

    def open_db_view(self):
        self.db = DbController(self.master, self.db_enabled)

    def copy_procedure(self):
        # checks if the copy_path is set, if the path is not set it will show an error message.
        # If everything is set correctly, the table will gets looped and all selected fileds will be appended
        # to an array of folders and files. After the loop is finished the first copy will start.
        # If the backup_path is also set, another copy will start.
        # If the coping is finished the status will get displayed with a messagebox

        # contains all files
        files_array = []
        # contains all folders
        folder_array = []
        # contains the selection of the table
        table_selection = self.view.table.selection()

        for selected_item in table_selection:
            # contains a single selection
            selected_path = self.get_path_from_table(selected_item)
            # contains the filepath without the root section
            file_path_without_root = self.get_file_path_without_root(self.root_path, selected_path)
            # adds the filepath without the root section to the files array
            files_array.append(file_path_without_root)
            # appends just the folder part to the folders array
            folder_array.append(
                file_path_without_root[:len(file_path_without_root) - len(os.path.basename(file_path_without_root))])
        # starts the copy process for the copy_path
        copy_status = self.copy_to_dest(folder_array, files_array, self.copy_path, "Kopierpfad wählen")
        # checks if the backup_path is set
        if not self.backup_path == "":
            # starts the copy process for the backup_path
            backup_status = self.copy_to_dest(folder_array, files_array, self.backup_path, "Backuppfad wählen")
            # checks the status of both copy processes
            if copy_status and backup_status:
                # shows a messagebox that all went fine
                self.view.show_messagebox("Info", "Kopieren Erfolgreich", "Die Daten wurden erfolgreich kopiert")
            else:
                # shows a messagebox that something went wrong
                self.view.show_messagebox("Error", "Kopieren Fehlgeschlagen",
                                          "Es ist ein Fehler beim Kopieren aufgetreten")
        else:
            # checks the copy status
            if copy_status:
                # shows a messagebox that all went fine
                self.view.show_messagebox("Info", "Kopieren Erfolgreich", "Die Daten wurden erfolgreich kopiert")

            else:
                # shows a messagebox that something went wrong
                self.view.show_messagebox("Error", "Kopieren Fehlgeschlagen",
                                          "Es ist ein Fehler beim Kopieren aufgetreten")
        # resets the Gui
        self.reset()

    def check_md5(self, files_array, dest_array, progressbar, label):
        # checks if the files_array and dest_array have the same length
        # otherwise it will return False and wont start checking md5.
        # if the arrays have equal length, the progressbar will turn yellow, the header text will change
        # and compares the md5 hash from the original and new file.
        # The function will return true or false depending on the end result

        # status gets used to check if everything went fine or not
        status = True
        # value gets used to set the value on the progressbar
        value = 0

        # checks if the arrays have the same length, otherwise something is wrong
        if len(files_array) == len(dest_array):
            # sets the progressbar to a different style
            self.view.change_progressbar_style(progressbar, "Yellow")
            # sets the value of the progressbar
            progressbar['value'] = value
            # sets the label header text of the gui section
            self.view.set_label_text(label, "Prüfe MD5 Hashes")
            # loop through the range of the arrays length
            for i in range(len(files_array)):
                try:
                    # creates a FileModel object for the src_file
                    src_file = FileModel(files_array[i])
                    src_file.calc_file_md5()
                    # sets the md5 hash of the src file
                    src_file_md5 = src_file.get_file_md5()
                    # creates a FileModel object for the dest_file
                    dest_file = FileModel(dest_array[i])
                    dest_file.calc_file_md5()
                    # sets the md5 hash of the copied file
                    dest_file_md5 = dest_file.get_file_md5()

                    if self.db is not None:
                        # original_path as text,    new_path as text,
                        # filename as text,         size as text,
                        # type as text,                md5 as text
                        self.db.insert(src_file.get_file_path(), dest_file.get_file_path(),
                                       dest_file.get_file_name(), dest_file.get_file_size_with_ident(),
                                       dest_file.get_file_type(), dest_file.get_file_md5())

                    # checks if the md5 hashes are not equal
                    if not src_file_md5 == dest_file_md5:
                        # sets the status to false and returns the status
                        status = False
                        return status
                    # if the md5 hashes are equal, the value gets incremented
                    value += 1
                    # sets the new value to the progressbar
                    self.view.update_progressbar(progressbar, value)
                except FileNotFoundError:
                    self.view.change_progressbar_style(progressbar, "red")
                    self.view.show_messagebox("Error", "Datei nicht gefunden",
                                              "Die Datei " + files_array[i] + " konnte nicht gefunden werden")
                    status = False
                    return status

        else:
            # sets the status to false
            status = False

        return status

    def copy_to_dest(self, folder_array, files_array, dest_path, dest_area):
        # copies files to dest_path and updates the progressbar.
        # after the loop the check_md5 method gets called with the two arrays
        # if the check_md5 return true, the progressbar will get a green color and shows a messagebox
        # else the progressbar gets a red color and shows a messagebox
        #
        # dest_area defines the area that gets showed on the gui

        # the progressbar and the label gets initialized and shows the progressbar
        if dest_area.lower() == "kopierpfad wählen":
            # progressbar gets used to set the value
            progressbar = self.view.progressbar_copy
            # label gets used to set the text of the header label
            label = self.view.label_copy
            label['text'] = "Kopieren"
            self.view.show_progressbar_copy()
        elif dest_area.lower() == "backuppfad wählen":
            # progressbar gets used to set the value
            progressbar = self.view.progressbar_backup
            # label gets used to set the text of the header label
            label = self.view.label_backup
            label['text'] = "Kopieren"
            self.view.show_progressbar_backup()
        else:
            self.view.show_messagebox("Error", "Error", "Es ist ein Fehler aufgetreten beim kopieren")
            return

        # sets the progressbar max value depending of the amount of files in the array
        self.set_progressbar_max_value(progressbar, len(files_array))
        # value contains the progressbar value
        value = 0
        # contains all the src files
        src_file_array = []
        # contains all the dest files
        dest_file_array = []
        # contains the status of the copy process
        status = True

        # creates directorys if they are not already existing
        for folder in folder_array:
            new_folder = os.path.join(dest_path, folder)
            if not os.path.exists(new_folder):
                self.makedirs(new_folder)

        for file in files_array:
            try:
                # sets the src_file path
                src_file = os.path.join(self.root_path, file)
                # sets the dest_file path
                dest_file = os.path.join(dest_path, file)
                # appends the src_file to the array
                src_file_array.append(src_file)
                # appends the dest_file to the array
                dest_file_array.append(dest_file)
                # checks if the dest_file exists
                if not os.path.exists(dest_file):
                    # copies the src_file to the new path
                    shutil.copy(src_file, dest_file)
                # increments the value
                value += 1
                # updates the progressbar value
                self.view.update_progressbar(progressbar, value)
            except FileNotFoundError:
                self.view.show_messagebox("Error", "Datei nicht gefunden",
                                          "Die Datei " + file + " konnte nicht gefunden werden")
                status = False
                return status
            except PermissionError:
                self.view.show_messagebox("Error", "Keine Zugriffsrechte",
                                          "Die Datei " + file + " konnte nicht kopiert werden")
                status = False
                return status
        # checks if the md5 check was successfully
        if self.check_md5(src_file_array, dest_file_array, progressbar, label):
            # sets the progressbar color to green
            self.view.change_progressbar_style(progressbar, "Green")
        else:
            # shows an error message and sets the progressbar color to red
            self.view.show_messagebox("Error", "MD5 check Fehlerhaft", "Beim MD5 Check trat ein Fehler auf")
            self.view.change_progressbar_style(progressbar, "Red")
            status = False

        return status

    @staticmethod
    def set_progressbar_max_value(progressbar, value):
        # gets used to set the max value of a progressbar
        progressbar['max'] = value

    @staticmethod
    def makedirs(dest):
        # creates direcotrys
        if not os.path.exists(dest):
            os.makedirs(dest)

    @staticmethod
    def get_file_path_without_root(root_path, full_path):
        # returns a path without the root_path
        return full_path[len(root_path) + 1:]

    def get_path_from_table(self, table_item):
        # returns the full filepath from the table
        return self.view.table.item(table_item)['values'][0]

    def select_path(self, dest_button):
        # is used to set the paths of the root, copy and backup variables
        if not self.thread_running:
            if dest_button['text'].lower() == "kopierpfad wählen":
                self.copy_path = self.view.get_folder_path()
                if not self.copy_path == "":
                    self.set_label_text(self.view.label_copy_path, "Kopierpfad: " + self.copy_path)
            elif dest_button['text'].lower() == "backuppfad wählen":
                self.backup_path = self.view.get_folder_path()
                if not self.backup_path == "":
                    self.set_label_text(self.view.label_backup_path, "Backuppfad: " + self.backup_path)
            elif dest_button['text'].lower() == "quelle wählen":
                self.root_path = self.view.get_folder_path()
                if not self.root_path == "":
                    # fills the array with the elements from the root folder
                    file_objects_array = self.get_all_files_from_folder(self.root_path)
                    # fills the table with the files
                    self.view.fill_table(file_objects_array)
                    self.reset()
            else:
                self.view.show_messagebox("Error", "Error ausgelöst von select_path function",
                                          "Es wurde ein falscher Button übergeben")

    def set_label_text(self, label_object, text):
        # sets the label text of the label_object
        self.view.set_label_text(label_object, text)

    def get_all_files_from_folder(self, path):
        self.view.table.delete(*self.view.table.get_children())
        # contains all the files
        files_array = []
        # collects all the files
        for root, dirs, files in os.walk(path):
            for file in files:
                # creates a new FileModel
                full_file = FileModel(os.path.join(root, file))
                # adds the FileModel to the array
                files_array.append(full_file)

        # returns the files_array
        return files_array

    def reset(self):
        # resets the gui elements
        self.copy_path = ""
        self.backup_path = ""
        self.view.reset_form()
        self.thread_running = False
