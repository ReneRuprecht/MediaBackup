from tkinter import Tk

from MediaBackup.controller import Controller

if __name__ == "__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()
