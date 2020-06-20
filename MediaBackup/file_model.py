import hashlib
import os
import pathlib
from os.path import basename


class FileModel:

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__file_name = basename(self.__file_path)
        self.__file_size_with_ident = 0
        self.__file_size = 0
        self.__file_md5 = 0
        self.__file_type = None

        self.__set_file_total_size()
        self.__set_file_type()

    def __set_file_type(self):
        self.__file_type = pathlib.Path(self.__file_path).suffix

    def get_file_type(self):
        return self.__file_type

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_file_size_with_ident(self):
        return self.__file_size_with_ident

    def get_file_size(self):
        return self.__file_size

    def get_file_md5(self):
        return self.__file_md5

    def __set_file_total_size(self):
        size = os.path.getsize(self.__file_path)
        self.__file_size = size
        if int(size / (1000 * 1000 * 1000)) > 0.0:
            self.__file_size_with_ident = str(round(size / (1000 * 1000 * 1000), 2)) + " GB"
        elif int(size / (1000 * 1000)) > 0.0:
            self.__file_size_with_ident = str(round(size / (1000 * 1000), 2)) + " MB"
        elif int(size / 1000) > 0.0:
            self.__file_size_with_ident = str(size / 1000) + " KB"
        else:
            self.__file_size_with_ident = str(size) + " B"

    def calc_file_md5(self):
        hash_md5 = hashlib.md5()
        with open(self.__file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        self.__file_md5 = hash_md5.hexdigest()
