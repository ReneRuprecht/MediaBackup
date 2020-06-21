import argparse
import sys
from tkinter import Tk

from MediaBackup.db_controller import DbController
from MediaBackup.main_controller import MainController

parser = argparse.ArgumentParser()
parser.add_argument('db_enabled', help='want to create a database (y or n)')
args = parser.parse_args()


def start(db_enabled, db_controller=None):
    root = Tk()
    root.wm_title("Main")
    # root.resizable(width=False, height=False)
    MainController(root, db_enabled, db_controller)
    root.mainloop()


if __name__ == "__main__":
    argument = sys.argv[1].lower()
    if argument[:1] == "y":
        # DbController call Frame=None but with db_enabled=True
        db_controller = DbController(None, True)
        # check if database is created without permission error
        if db_controller.get_error_message() == "":
            # start the application with db_enabled=True and the db controller
            start(True, db_controller)

    elif argument[:1] == "n":
        # start the applictation without database
        start(False)
    else:
        parser.print_help()
