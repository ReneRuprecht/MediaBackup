from tkinter import Tk

from MediaBackup.main_controller import Controller

if __name__ == "__main__":
    root = Tk()
    # root.resizable(width=False, height=False)
    app = Controller(root)
    root.mainloop()
