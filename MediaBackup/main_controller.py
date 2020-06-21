import os
import shutil
import threading

from .db_controller import DbController
from .db_model import DbModel
from .file_model import FileModel
from .main_view import MainView


class MainController:
    def __init__(self, master, db_enabled=False, db=None):
        self.view = MainView(master, self)
        self.db_view = None
        self.master = master
        self.db_controller = None
        self.db_enabled = db_enabled
        # check if db is enabled and a db object was created
        if db_enabled and db is not None:
            self.db_enabled = db_enabled
            self.db_controller = db
            self.view.show_db_button()
        # contains just the root section of the loaded directory
        self.root_path = ""
        self.copy_path = ""
        self.backup_path = ""
        # will contain the thread object
        self.copy_to_dests_thread = None
        # contains if a thread is running, to prevent double execution
        self.thread_running = False

    def start_copy_thread(self):

        # checks if a thread is already running, to prevent the user from starting more than one operation
        # checks if everything that is needed is set.
        # if there is not thread running it will start a new thread.

        # check if thread is already running
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

    def copy_procedure(self):
        # grabs alls the selected items from the table.
        # loops through the selected items, extracted the root folder out of the filepath into the
        # file_path_without_root and the folder-only part without the filename into the folder_array.
        # sets the progressbar and label to the corresponding gui elements.
        # starts the copy process. it will display an error message if something went wrong otherwise
        # the md5 check will start. the md5 check will also display an error message if something went wrong.
        # if all went fine and the backup path is set the procedure will start copy and md5 check in
        # the same way as before. after that a message will display if the process went fine or not

        # contains all files
        files_array = []
        # contains all folders for the mkdir
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

        # progressbar gets used in the copy_to_dest function
        progressbar = self.view.progressbar_copy
        # label gets used to set the text of the header label
        label = self.view.label_copy
        self.view.set_label_text(label, "Kopieren")
        # shows the progressbar on the kopieren side of the guid
        self.view.show_progressbar_copy()
        self.set_progressbar_max_value(progressbar, len(files_array))
        # starts the copy process for the copy_path
        copy_status, error, src_file_array, dest_file_array = self.copy_to_dest(folder_array, files_array,
                                                                                self.copy_path,
                                                                                progressbar)

        # if the copy_status is true, that means the copy process went fine
        if copy_status:
            # sets the label text to the new heading
            self.view.set_label_text(self.view.label_copy, "Prüfe MD5 Hashes")
            # starts the md5 check
            md5_status, error = self.check_md5(src_file_array, dest_file_array, progressbar)
            if md5_status:
                self.view.set_progressbar_style(progressbar, "Green")
                self.view.set_label_text(self.view.label_copy, "Kopieren erfolgreich")
            else:
                self.view.set_progressbar_style(progressbar, "Red")
                self.view.set_label_text(self.view.label_copy, "MD5 check Fehlerhaft")
                self.view.show_messagebox("Error", "MD5 check Fehlerhaft", error)
                self.reset(True)
                return
        else:
            self.view.set_progressbar_style(progressbar, "Red")
            self.view.set_label_text(self.view.label_copy, "Kopieren Fehlgeschlagen")
            self.view.show_messagebox("Error", "Kopieren Fehlgeschlagen",
                                      error)
            self.reset(True)
            return

        # checks if the backup_path is set
        if self.backup_path != "":
            # progressbar gets used in the copy_to_dest function
            progressbar = self.view.progressbar_backup
            # label gets used to set the text of the header label
            label = self.view.label_backup
            self.view.set_label_text(label, "Kopieren")
            # shows the progressbar on the backup side of the guid
            self.view.show_progressbar_backup()
            self.set_progressbar_max_value(progressbar, len(files_array))
            # starts the copy process for the backup_path
            backup_status, error, src_file_array, dest_file_array = self.copy_to_dest(folder_array, files_array,
                                                                                      self.backup_path, progressbar)
            # if the backup_status is true, that means the copy process went fine
            if backup_status:
                # sets the label text to the new heading
                self.view.set_label_text(self.view.label_backup, "Prüfe MD5 Hashes")
                # starts the md5 check
                md5_status, error = self.check_md5(src_file_array, dest_file_array, progressbar)
                if md5_status:
                    self.view.set_label_text(self.view.label_backup, "Kopieren erfolgreich")
                    self.view.set_progressbar_style(progressbar, "Green")
                else:
                    self.view.set_progressbar_style(progressbar, "Red")
                    self.view.set_label_text(self.view.label_backup, "MD5 check Fehlerhaft")
                    self.view.show_messagebox("Error", "MD5 check Fehlerhaft", error)
                    self.reset(True)
                    return
            else:
                self.view.set_progressbar_style(progressbar, "Red")
                self.view.set_label_text(self.view.label_backup, "Kopieren Fehlgeschlagen")
                self.view.show_messagebox("Error", "Kopieren Fehlgeschlagen",
                                          error)
                self.reset(True)
                return

            # everything is finished with the backup path set
            self.view.show_messagebox("Info", "Kopieren Erfolgreich", "Die Daten wurden erfolgreich kopiert")

        else:
            # everything is finished without the backup path set
            if copy_status:
                self.view.set_label_text(self.view.label_copy, "Kopieren erfolgreich")
                self.view.set_progressbar_style(progressbar, "Green")
                # shows a messagebox that all went fine
                self.view.show_messagebox("Info", "Kopieren Erfolgreich", "Die Daten wurden erfolgreich kopiert")
            else:
                self.view.set_label_text(self.view.label_copy, "Kopieren Fehlgeschlagen")
                self.view.set_progressbar_style(progressbar, "Red")
                # shows a messagebox that something went wrong
                self.view.show_messagebox("Error", "Kopieren Fehlgeschlagen",
                                          "Es ist ein Fehler beim Kopieren aufgetreten")
        # resets the Gui
        self.reset()

    def copy_to_dest(self, folder_array, files_array, dest_path, progressbar=None):
        # copies files to dest_path.
        # changes the value of a progressbar if there is one given to this function
        # returns true, src_file_array and the dest_file_array if everything went fine
        # else an error will be displayed and return false

        # value contains the progressbar value
        value = 0
        # contains all the src files
        src_file_array = []
        # contains all the dest files
        dest_file_array = []

        error = ""

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
                else:
                    tmp_src_array = [src_file]
                    tmp_dest_array = [dest_file]
                    if not self.check_md5(tmp_src_array, tmp_dest_array):
                        new_file_name = str(file).split('.')[0] + "_old"
                        new_file_name_ext = "." + str(file).split('.')[1]
                        os.rename(dest_file, os.path.join(dest_path, new_file_name + new_file_name_ext))
                        shutil.copy(src_file, dest_file)
                # checks if a progressbar is set
                if progressbar is not None:
                    # increments the value
                    value += 1
                    # updates the progressbar value
                    self.view.update_progressbar_value(progressbar, value)
            except FileNotFoundError:
                error = "Die Datei " + file + " konnte nicht gefunden werden"
                # self.view.show_messagebox("Error", "Datei nicht gefunden",
                #                         "Die Datei " + file + " konnte nicht gefunden werden")

                return False, error, [], []
            except PermissionError:
                error = "Die Datei " + file + " konnte nicht kopiert werden"
                # self.view.show_messagebox("Error", "Keine Zugriffsrechte",
                #                         "Die Datei " + file + " konnte nicht kopiert werden")

                return False, error, [], []

        return True, error, src_file_array, dest_file_array

    def check_md5(self, src_files_array, dest_files_array, progressbar=None):
        # checks if the files_array and dest_array have the same length
        # otherwise it will return False and wont start checking md5.
        # if the arrays have equal length, the progressbar will turn yellow, the header text will change
        # and compares the md5 hash from the original and new file.
        # The function will return true or false depending on the end result

        # value is used to set the value on the progressbar
        value = 0

        error = ""

        # checks if the arrays have the same length, otherwise something is wrong
        if len(src_files_array) == len(dest_files_array):
            # sets the progressbar to a different style
            if progressbar is not None:
                self.view.set_progressbar_style(progressbar, "Yellow")
                # sets the value of the progressbar
                progressbar['value'] = value
                # loop through the range of the arrays length
            for i in range(len(src_files_array)):
                try:
                    # creates a FileModel object for the src_file
                    src_file = FileModel(src_files_array[i])
                    src_file.calc_file_md5()
                    # sets the md5 hash of the src file
                    src_file_md5 = src_file.get_file_md5()
                    # creates a FileModel object for the dest_file
                    dest_file = FileModel(dest_files_array[i])
                    dest_file.calc_file_md5()
                    # sets the md5 hash of the copied file
                    dest_file_md5 = dest_file.get_file_md5()

                    # checks if the md5 hashes are not equal
                    if src_file_md5 != dest_file_md5:
                        # sets the status to false and returns the status
                        status = False
                        error = "Der MD5 Hash stimmt nicht mit der Quelldatei überein"
                        return status, error
                    # if the md5 hashes are equal, the value gets incremented
                    value += 1

                    # checks if there is a DbController
                    if self.db_controller is not None:
                        db_object = DbModel(src_file.get_file_path(), dest_file.get_file_path(),
                                            dest_file.get_file_name(), dest_file.get_file_size_with_ident(),
                                            dest_file.get_file_type(), dest_file.get_file_md5())

                        self.db_controller.insert(db_object)

                    if progressbar is not None:
                        # sets the new value to the progressbar
                        self.view.update_progressbar_value(progressbar, value)

                except FileNotFoundError:
                    error = "Die Datei " + src_files_array[i] + " konnte nicht gefunden werden"
                    return False, error

        else:
            error = "Die Daten sind nicht vollständig"
            return False, error

        return True, error

    def open_db_view(self):
        self.db_controller = DbController(self.master, self.db_enabled)

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
                self.copy_path = self.view.get_folder_path_from_file_dialog()
                if self.copy_path != "":
                    self.set_label_text(self.view.label_copy_path, "Kopierpfad: " + self.copy_path)
            elif dest_button['text'].lower() == "backuppfad wählen":
                self.backup_path = self.view.get_folder_path_from_file_dialog()
                if self.backup_path != "":
                    self.set_label_text(self.view.label_backup_path, "Backuppfad: " + self.backup_path)
            elif dest_button['text'].lower() == "quelle wählen":
                self.root_path = self.view.get_folder_path_from_file_dialog()
                if self.root_path != "":
                    # fills the array with the elements from the root folder
                    file_objects_array = self.get_all_files_from_folder(self.root_path)
                    # fills the table with the files
                    self.view.fill_table(file_objects_array)
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

    def reset(self, full=False):
        if full:
            self.view.clear_table()

        # resets the gui elements
        self.copy_path = ""
        self.backup_path = ""
        self.view.reset_form()
        self.thread_running = False
