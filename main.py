from PySide6.QtWidgets import QApplication

from database import create_db
from windows.main_window import Window


create_db()

app = QApplication()
win = Window()
win.show()
app.exec()