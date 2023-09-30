from PySide6.QtWidgets import QApplication

from initdb.initdatabase import create_db
from windows.main_window import Window


def run():
    create_db()
    app = QApplication()
    win = Window()
    win.show()
    app.exec()


if __name__ == "__main__":
    run()