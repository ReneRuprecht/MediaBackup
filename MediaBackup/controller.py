from .view import View


class Controller:
    def __init__(self, master):
        View(master)

    def print(self):
        print("1")
