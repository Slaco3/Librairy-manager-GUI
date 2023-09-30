from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox, QLabel


from models.book import get_borrowed_books_from_db
from models.borrower import get_borrower_with_id


class GiveBackTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        self.populate_lw_borrowed_book()

    def create_widgets(self):
        self.label_borrowed_book = QLabel("Liste des livres empruntés :")
        self.lw_borrowed_book = QListWidget()
        self.btn_give_back_book = QPushButton("Récupérer le livre")

    def setup_layouts(self):
        self.tab4_layout = QVBoxLayout(self) 
        self.tab4_layout.addWidget(self.label_borrowed_book)
        self.tab4_layout.addWidget(self.lw_borrowed_book)
        self.tab4_layout.addWidget(self.btn_give_back_book)

    def setup_connections(self):
        self.btn_give_back_book.clicked.connect(self.recover_book)

    def populate_lw_borrowed_book(self):
        books = get_borrowed_books_from_db()
        for book in books:
            borrower = get_borrower_with_id(book.borrower_id)
            lw_item = QListWidgetItem(book.title.title() + " de " + book.author.upper() + " (" + borrower.first_name.title() + " " + borrower.last_name.upper() + ")")
            lw_item.book = book
            lw_item.borrower = borrower
            self.lw_borrowed_book.addItem(lw_item)

    def recover_book(self):
        item = self.lw_borrowed_book.currentItem()
        if not item:
            return
        
        book = item.book
        borrower = item.borrower

        book.borrower_id = None
        borrower.book_id = None

        book.update_borrower_id_in_db(book.borrower_id)
        borrower.update_book_id_in_db(borrower.book_id)

        QMessageBox.information(self,"Livre bien récupéré", f"{borrower.first_name.title()} {borrower.last_name.upper()} a bien rendu le livre suivant : {book.title.title()}")
        self.lw_borrowed_book.clear()
        self.populate_lw_borrowed_book()
