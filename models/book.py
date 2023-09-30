from initdb.initdatabase import PATH_DB, open_db_and_create_cursor


def create_books_with_tuples_db_datas(tuples_books):
    books = []
    for tuple_book in tuples_books:
        book = Book(title=tuple_book[1], author=tuple_book[2], publication_date=tuple_book[3],borrower_id=tuple_book[4], id=tuple_book[0])
        books.append(book)
    return books


def get_books_from_db():
    conn, cursor = open_db_and_create_cursor()
    cursor.execute("SELECT * FROM books")
    tuples_books = cursor.fetchall()
    conn.close()
    return create_books_with_tuples_db_datas(tuples_books)
    

def get_free_books_from_db():
    conn, cursor = open_db_and_create_cursor()
    cursor.execute("SELECT * FROM books WHERE borrower_id IS NULL")
    tuples_books = cursor.fetchall()
    conn.close()
    return create_books_with_tuples_db_datas(tuples_books)


def get_borrowed_books_from_db():
    conn, cursor = open_db_and_create_cursor()
    cursor.execute("SELECT * FROM books WHERE borrower_id IS NOT NULL")
    tuples_books = cursor.fetchall()
    conn.close()
    return create_books_with_tuples_db_datas(tuples_books)


class Book:
    def __init__(self, title, author, publication_date, borrower_id=None, id=None):
        self.title = title.lower()
        self.author = author.lower()
        self.publication_date = publication_date
        self.borrower_id = borrower_id
        self.id = id

    def __repr__(self):
        return self.title
    
    def _get_books_titles_list_from_db(self):
        books = get_books_from_db()
        books_titles = [book.title for book in books]
        return books_titles
    
    def save_in_db(self):
        books_titles = self._get_books_titles_list_from_db()
        if self.title in books_titles:
            return False
        
        conn, cursor = open_db_and_create_cursor()
        cursor.execute("INSERT INTO books (title, author, publication_date) VALUES(?,?,?)",(self.title, self.author, self.publication_date))
        conn.commit()
        conn.close()
        return True

    def delete_in_db(self):
        conn, cursor = open_db_and_create_cursor()
        cursor.execute("DELETE FROM books WHERE title=?", (self.title,))
        conn.commit()
        conn.close()
    
    def update_borrower_id_in_db(self, new_id):
        conn, cursor = open_db_and_create_cursor()
        cursor.execute("UPDATE books SET borrower_id = ? WHERE title=?",(new_id, self.title))
        conn.commit()
        conn.close()






