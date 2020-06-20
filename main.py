import argparse
import sys
from tkinter import Tk

from MediaBackup.db_controller import DbController
from MediaBackup.main_controller import MainController

parser = argparse.ArgumentParser()
parser.add_argument('db', help='want to create a database (y or n)')
args = parser.parse_args()

if __name__ == "__main__":
    db_enabled = sys.argv[1].lower()
    db = None
    if db_enabled[:1] == "y" or db_enabled[:1] == "j":
        db_enabled = True
        db = DbController()
    else:
        db_enabled = False

    root = Tk()
    # root.resizable(width=False, height=False)
    app = MainController(root, db_enabled, db)
    root.mainloop()
