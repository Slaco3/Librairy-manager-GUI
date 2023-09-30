from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QMessageBox
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt

from borrower import Borrower, get_borrowers_from_db


class BorrowerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        self.setup_shortcuts()
        self.populate_lw_borrower()

    def create_widgets(self):
        self.le_addborrower = QLineEdit()
        self.le_addborrower.setPlaceholderText("Entrez le nom du client à ajouter...")
        self.btn_addborrower = QPushButton("Ajouter")
        self.lw_borrower = QListWidget()
        self.btn_sort_by_name = QPushButton("Trier les client par nom")
    
    def setup_layouts(self):
            self.tab2_layout = QVBoxLayout(self)
            self.tab2_layout.addWidget(self.le_addborrower)
            self.tab2_layout.addWidget(self.btn_addborrower)
            self.tab2_layout.addWidget(self.lw_borrower)
            self.tab2_layout.addWidget(self.btn_sort_by_name)

    def setup_connections(self):
         self.btn_addborrower.clicked.connect(self.enter_borrower_in_lw_borrowers)
         self.btn_sort_by_name.clicked.connect(self.dispay_borrower_by_name)

    def setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key_Return), self.le_addborrower, self.enter_borrower_in_lw_borrowers)
        QShortcut(QKeySequence(Qt.Key_Delete), self.lw_borrower, self.delete_borrower_in_lw_borrowers)

    def add_borrower_in_lw_borrower(self, borrower):
        lw_item = QListWidgetItem(borrower.last_name.upper() + " " + borrower.first_name.title())
        lw_item.borrower = borrower
        self.lw_borrower.addItem(lw_item)

    def enter_borrower_in_lw_borrowers(self):
        last_name = self.le_addborrower.text()
        if not last_name:
             return
        first_name, result_first_name = QInputDialog.getText(self, "Ajouter le prénom du client", "Entrez le prénom du client :")
        if not first_name or not result_first_name:
            return
        birth_date, result_birth_date = QInputDialog.getInt(self, "Ajouter l'année de naissance du client", "Entrez l'année de naissance du client :", 2000,1900,2100)
        if not birth_date or not result_birth_date:
            return
        borrower = Borrower(last_name.lower().strip(), first_name.lower().strip(), birth_date)
        if borrower.save_in_db():
            self.add_borrower_in_lw_borrower(borrower)
        else:
            QMessageBox.information(self, "Client déjà existant", "Ce client existe déjà dans la base.")
        self.le_addborrower.clear()

    def delete_borrower_in_lw_borrowers(self):
        item = self.lw_borrower.currentItem()
        if item.borrower.book_id is not None:
            QMessageBox.information(self, "Impossible de supprimer le client", "Ce client n'a pas rendu le livre qu'il a emprunté, vous ne pouvez pas le supprimer")
            return
        item.borrower.delete_in_db()
        self.lw_borrower.takeItem(self.lw_borrower.row(item))

    def populate_lw_borrower(self):
        borrowers = get_borrowers_from_db()
        for borrower in borrowers:
            self.add_borrower_in_lw_borrower(borrower)
    
    def dispay_borrower_by_name(self):
        self.lw_borrower.clear()
        borrowers = get_borrowers_from_db()
        borrowers.sort(key=lambda e: e.last_name)
        for borrower in borrowers:
            self.add_borrower_in_lw_borrower(borrower)