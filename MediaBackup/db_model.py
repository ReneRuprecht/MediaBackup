class DbModel:

    def __init__(self, original_path, new_path, filename, size, type, md5):
        self.__original_path = original_path
        self.__new_path = new_path
        self.__filename = filename
        self.__size = size
        self.__type = type
        self.__md5 = md5

    def get_object_dict(self):
        return {'original_path': self.__original_path, 'new_path': self.__new_path,
                'filename': self.__filename, 'size': self.__size,
                'type': self.__type, 'md5': self.__md5}

    def get_original_path(self):
        return self.__original_path

    def get_new_path(self):
        return self.__new_path

    def get_filename(self):
        return self.__filename

    def get_size(self):
        return self.__size

    def get_type(self):
        return self.__type

    def get_md5(self):
        return self.__md5
