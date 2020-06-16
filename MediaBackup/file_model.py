import hashlib
import os
from os.path import basename


class FileModel:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = basename(self.__file_path)
        self.__file_size = 0
        self.__file_md5 = 0

        self.calc_file_total_size()
        self.calc_file_md5()

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_file_size(self):
        return self.__file_size

    def get_file_md5(self):
        return self.__file_md5

    def calc_file_total_size(self):
        self.__file_size = os.path.getsize(self.__file_path)

    def calc_file_md5(self):
        hash_md5 = hashlib.md5()
        with open(self.__file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.__file_md5 = hash_md5.hexdigest()
