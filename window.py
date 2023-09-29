from typing import Optional
from PySide6.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QTabWidget, QLabel
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt

from book import Book, get_books_from_db, get_free_books_from_db, get_borrowed_books_from_db
from borrower import Borrower, get_borrowers_from_db, get_borrower_with_id, get_borrower_by_last_name_and_first_name_from_db


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


class GiveBackTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setup_layouts()
        self.setup_connections()
        self.populate_lw_borrowed_book()

    def create_widgets(self):
        self.label_borrowed_book = QLabel("Liste des livres empruntés")
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
            lw_item = QListWidgetItem(book.title.title() + " de " + book.author.upper() + " (" + borrower.first_name.title() + " " + borrower.last_name.upper() + " )")
            lw_item.book = book 
            self.lw_borrowed_book.addItem(lw_item)

    def recover_book(self):
        item = self.lw_borrowed_book.currentItem()
        if not item:
            return
        book = item.book
        borrower = get_borrower_with_id(book.borrower_id)
        book.borrower_id = None
        borrower.book_id = None
        book.update_borrower_id_in_db(book.borrower_id)
        borrower.update_book_id_in_db(borrower.book_id)
        QMessageBox.information(self,"Livre bien récupéré", f"{borrower.first_name.title()} {borrower.last_name.upper()} a bien rendu le livre suivant : {book.title.title()}")
        self.lw_borrowed_book.clear()
        self.populate_lw_borrowed_book()



       
        


