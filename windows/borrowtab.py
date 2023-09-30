
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QLabel


from models.book import get_free_books_from_db
from models.borrower import get_borrower_by_last_name_and_first_name_from_db



class BorrowTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        # self.setup_shortcuts()
        self.populate_lw_free_books()

    def create_widgets(self):
        self.label_free_book = QLabel("Liste des livres disponibles")
        self.lw_free_book = QListWidget()
        self.btn_borrow_book = QPushButton("Prêter le livre")

    def setup_layouts(self):
        self.tab3_layout = QVBoxLayout(self) 
        self.tab3_layout.addWidget(self.label_free_book)
        self.tab3_layout.addWidget(self.lw_free_book)
        self.tab3_layout.addWidget(self.btn_borrow_book)

    def setup_connections(self):
        self.btn_borrow_book.clicked.connect(self.borrow_book)

    def borrow_book(self):
        if not self.lw_free_book.currentItem():
            return
        last_name, last_name_result = QInputDialog.getText(self, "Nom du client emprunteur", "Entrer le nom du client")

        first_name, first_name_result = QInputDialog.getText(self, "Prénom du client emprunteur", "Entrer le prénom du client")

        if last_name and last_name_result and first_name and first_name_result:
            try:
                borrower = get_borrower_by_last_name_and_first_name_from_db(last_name.lower().strip(), first_name.lower().strip())
            except TypeError:
                print("Ce client n'existe pas")
                QMessageBox.information(self,"Client inconnu", "Ce client n'existe pas")
                return
            if borrower.book_id is not None:
                print("Ce client possède déjà un livre")
                QMessageBox.information(self,"Prêt impossible", "Ce client a déja emprunté un livre")
                return
        else:
            return
        item = self.lw_free_book.currentItem()
        book = item.book
        print(borrower.__dict__)

        book.borrower_id = borrower.id
        borrower.book_id = book.id

        book.update_borrower_id_in_db(borrower.id)
        borrower.update_book_id_in_db(book.id)
        
        QMessageBox.information(self,"Prêt bien effectué", f"Le client {borrower.first_name.title()} {borrower.last_name.upper()} a bien emprunté le livre : {book.title.title()}")
        self.lw_free_book.clear()
        self.populate_lw_free_books()

    def populate_lw_free_books(self):
        books = get_free_books_from_db()
        for book in books:
            lw_item = QListWidgetItem(book.title.title() + " de " + book.author.upper())
            lw_item.book = book 
            self.lw_free_book.addItem(lw_item)