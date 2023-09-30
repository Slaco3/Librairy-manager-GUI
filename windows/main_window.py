from PySide6.QtWidgets import QMainWindow, QTabWidget

from .bookstab import BooksTab
from .borrowtab import BorrowTab
from .borrowertab import BorrowerTab
from .givebacktab import GiveBackTab


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Librairy manager")
        self.resize(500, 600)
        self.create_widgets()
        
    def create_widgets(self):
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        self.tab1 = BooksTab()
        self.tab2 = BorrowerTab()
        self.tab3 = BorrowTab()
        self.tab4 = GiveBackTab()

        self.central_widget.addTab(self.tab1, "Ma bibliothèque")
        self.central_widget.addTab(self.tab2, "Mes clients")
        self.central_widget.addTab(self.tab3, "Prêt des livres")
        self.central_widget.addTab(self.tab4, "Retour des livres")

        self.central_widget.currentChanged.connect(self.tab_change)

    def tab_change(self, index):
        if index == 0:
            self.tab1.lw_books.clear()
            self.tab1.populate_lw_books()

        if index == 1:
            self.tab2.lw_borrower.clear()
            self.tab2.populate_lw_borrower()

        if index == 2:
            self.tab3.lw_free_book.clear()
            self.tab3.populate_lw_free_books()

        if index == 3:
            self.tab4.lw_borrowed_book.clear()
            self.tab4.populate_lw_borrowed_book()