from PySide6.QtWidgets import QApplication

from database import PATH_DB, create_db
from window import Window

create_db()

app = QApplication()
win = Window()
win.show()
app.exec()