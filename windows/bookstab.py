from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QMessageBox
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt

from book import Book, get_books_from_db


class BooksTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        self.setup_shortcuts()
        self.populate_lw_books()

    def create_widgets(self):
        self.le_addbook = QLineEdit()
        self.le_addbook.setPlaceholderText("Entrez le titre du livre à ajouter...")
        self.btn_addbook = QPushButton("Ajouter")
        self.lw_books = QListWidget()

    def setup_layouts(self):
        self.tab1_layout = QVBoxLayout(self) 
        self.tab1_layout.addWidget(self.le_addbook)
        self.tab1_layout.addWidget(self.btn_addbook)
        self.tab1_layout.addWidget(self.lw_books)
        
    def setup_connections(self):
            self.btn_addbook.clicked.connect(self.enter_book_in_lw_books)

    def setup_shortcuts(self):
            QShortcut(QKeySequence(Qt.Key_Return), self.le_addbook, self.enter_book_in_lw_books)
            QShortcut(QKeySequence(Qt.Key_Delete), self.lw_books, self.delete_book_in_lw_books)

    def add_book_in_lw_books(self, book):
        lw_item = QListWidgetItem(book.title.title() + " de " + book.author.upper())
        lw_item.book = book
        self.lw_books.addItem(lw_item)
         
    def enter_book_in_lw_books(self):
        title = self.le_addbook.text()
        if not title:
             return
        author, result_author = QInputDialog.getText(self, "Ajouter un auteur", "Entrez le nom de l'auteur :")
        if not author or not result_author:
            return
        publication_date, result_date = QInputDialog.getInt(self, "Ajouter une date de publication", "Entrez la date de publication :", 2000, -3500, 2100)
        if not publication_date or not result_date:
            return
        book = Book(title.lower().strip(), author.lower().strip(), publication_date)
        if book.save_in_db():
            self.add_book_in_lw_books(book)
        else:
            QMessageBox.information(self, "Livre déjà existant", "Ce livre existe déjà dans la bibliothèque.")
        self.le_addbook.clear()
        
    def delete_book_in_lw_books(self):
        item = self.lw_books.currentItem()
        if item.book.borrower_id:
            QMessageBox.information(self, "Impossible de supprimer le livre", "Ce livre n'a pas été rendu vous ne pouvez pas le supprimer.")
            return
        item.book.delete_in_db()
        self.lw_books.takeItem(self.lw_books.row(item))

    def populate_lw_books(self):
        books = get_books_from_db()
        for book in books:
            self.add_book_in_lw_books(book) 