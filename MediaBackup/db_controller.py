import sqlite3

from MediaBackup.db_model import DbModel
from MediaBackup.db_view import DbView


class DbController:
    def __init__(self, master=None, db_enabled=False):
        self.db_name = "MediaBackup.db"
        # contains error if a permissionerror will rise
        self.__error = ""
        # contains the choice if the user wants to create a database
        self.db_enabled = db_enabled

        if self.db_enabled:
            # trys to create the database otherwise it will rise an exception
            try:
                self.db = sqlite3.connect(self.db_name)
            except PermissionError:
                self.__error = "Die Datenbank konnte nicht erstellt werden aufgrund von fehlenden Zugriffsrechten."
                self.display_error_on_console()
                return

            self.cursor = self.db.cursor()
            # check if the table exists
            self.cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table' AND name='files'; ''')
            exists = False
            elements = self.cursor.fetchall()
            if len(elements) >= 1:
                exists = True

            # if the table does not exists, create the table
            if not exists:
                self.cursor.execute("""CREATE TABLE files (
                                            original_path text,
                                            new_path text,
                                            filename text,
                                            size text,
                                            type text,
                                            md5 text
                                        )""")
                self.db.commit()
                self.db.close()

        # set the view only if a frame is given
        if master is not None:
            self.db_view = DbView(master, self)

    def display_error_on_console(self):
        # displays the error on the console
        if self.__error != "":
            print(self.__error)

    def get_error_message(self):
        # returns the error, is used in the main.py to check if database is created
        return self.__error

    def fill_table(self):
        # gets all database items and fills the table in the view
        db_object_array = self.get_all_data()
        self.db_view.fill_table(db_object_array)

    # original_path, new_path, filename, size, file_type, md5
    def insert(self, db_object):
        db_object_dict = db_object.get_object_dict()

        # inserts a new entry into the database if the entry does not exists
        if not self.check_if_data_exists(db_object):
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO files VALUES('{}','{}', '{}','{}', '{}','{}');".format(db_object_dict['original_path'],
                                                                                    db_object_dict['new_path'],
                                                                                    db_object_dict['filename'],
                                                                                    db_object_dict['size'],
                                                                                    db_object_dict['type'],
                                                                                    db_object_dict['md5']))
            db.commit()
            cursor.close()
        # else:
        #    print("Data existiert bereits")

    def check_if_data_exists(self, db_object):
        db_object_dict = db_object.get_object_dict()
        # checks if the data exists that the user wants to add
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM files WHERE original_path='{}' AND new_path='{}'  AND filename='{}'"
            " AND size='{}' AND type='{}' AND md5='{}';".format(
                db_object_dict['original_path'],
                db_object_dict['new_path'],
                db_object_dict['filename'],
                db_object_dict['size'],
                db_object_dict['type'],
                db_object_dict['md5']))
        exists = False
        elements = cursor.fetchall()
        if len(elements) >= 1:
            exists = True
        db.commit()
        cursor.close()

        return exists

    def get_all_data(self):
        # returns an db object array with all entrys from the database
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM files;")
        elements = cursor.fetchall()

        db_object_array = []
        for i in elements:
            db_object = DbModel(i[0], i[1],
                                i[2], i[3],
                                i[4], i[5]
                                )

            db_object_array.append(db_object)
        db.commit()
        cursor.close()
        return db_object_array
