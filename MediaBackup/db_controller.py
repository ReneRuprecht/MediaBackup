import sqlite3

from MediaBackup.db_view import DbView


class DbController:
    def __init__(self, master=None, db_enabled=False):

        self.db_enabled = db_enabled
        if self.db_enabled:
            self.db = sqlite3.connect('test.db')
            self.cursor = self.db.cursor()

            self.cursor.execute(''' SELECT name FROM sqlite_master WHERE type='table' AND name='test'; ''')

            exists = False
            elements = self.cursor.fetchall()
            if len(elements) >= 1:
                exists = True

            if not exists:
                self.cursor.execute("""CREATE TABLE test (
                                            original_path text,
                                            new_path text,
                                            filename text,
                                            size text,
                                            type text,
                                            md5 text
                                        )""")
                self.db.commit()
                self.db.close()
        if master is not None:
            self.db_view = DbView(master, self)

    def fill_table(self):
        print("1")
        db_object_array = self.get_all_data()
        self.db_view.fill_table(db_object_array)

    def insert(self, original_path, new_path, filename, size, file_type, md5):

        if not self.check_if_data_exists(original_path, new_path, filename, size, file_type, md5):
            db = sqlite3.connect('test.db')
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO test VALUES('{}','{}', '{}','{}', '{}','{}');".format(original_path, new_path, filename, size,
                                                                                   file_type,
                                                                                   md5))
            db.commit()
            cursor.close()
        else:
            print("Data existiert bereits")

    @staticmethod
    def check_if_data_exists(original_path, new_path, filename, size, file_type, md5):
        db = sqlite3.connect('test.db')
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM test WHERE original_path='{}' AND new_path='{}'  AND filename='{}'"
            " AND size='{}' AND type='{}' AND md5='{}';".format(
                original_path, new_path
                , filename, size, file_type,
                md5))

        exists = False
        elements = cursor.fetchall()
        if len(elements) >= 1:
            exists = True

        db.commit()
        cursor.close()

        return exists

    @staticmethod
    def get_all_data():
        db = sqlite3.connect('test.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM test;")
        elements = cursor.fetchall()
        db_object_array = []
        for i in elements:
            dbx = {'original_path': i[0], 'new_path': i[1], 'filename': i[2], 'size': i[3], 'type': i[4],
                   'md5': i[5]}
            db_object_array.append(dbx)
        db.commit()
        cursor.close()
        return db_object_array
