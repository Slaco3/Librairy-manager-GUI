import sqlite3
from initdb.initdatabase import PATH_DB


def get_borrowers_from_db():
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrower")
    tuples_borrowers = cursor.fetchall()
    conn.close()
    borrowers = []
    for tuple_borrower in tuples_borrowers:
        borrower = Borrower(tuple_borrower[1], tuple_borrower[2], tuple_borrower[3],tuple_borrower[4], tuple_borrower[0])
        borrowers.append(borrower)
    return borrowers


def get_borrower_by_last_name_and_first_name_from_db(last_name, first_name):
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrower WHERE last_name=? AND first_name=? ", (last_name, first_name))
    tuple_borrower = cursor.fetchone()
    conn.close()
    borrower = Borrower(tuple_borrower[1], tuple_borrower[2], tuple_borrower[3], tuple_borrower[4], tuple_borrower[0])
    return borrower


def get_borrower_with_id(id):
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM borrower WHERE id=?", (id,))
    tuple_borrower = cursor.fetchone()
    conn.close()
    borrower = Borrower(tuple_borrower[1], tuple_borrower[2], tuple_borrower[3], tuple_borrower[4], tuple_borrower[0])
    return borrower


class Borrower:
    def __init__(self, last_name, first_name, birth_date, book_id=None, id=None):
        self.last_name = last_name.lower()     
        self.first_name = first_name.lower()    
        self.birth_date = birth_date 
        self.book_id = book_id
        self.id = id

    def __repr__(self):
        return self.last_name 

    def exist_in_db(self):
        conn = sqlite3.connect(PATH_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM borrower WHERE last_name = ? AND first_name = ?", (self.last_name, self.first_name))
        existing_borrower = cursor.fetchone()
        conn.close()
        if existing_borrower:
            return True

    def save_in_db(self):
        if self.exist_in_db():
            return False  
               
        conn = sqlite3.connect(PATH_DB)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO borrower (last_name, first_name, birth_date) VALUES (?,?,?)",(self.last_name, self.first_name,self.birth_date))
        conn.commit()
        conn.close()
        return True

    def delete_in_db(self):
        conn = sqlite3.connect(PATH_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM borrower WHERE last_name=?", (self.last_name,))
        conn.commit()
        conn.close()

    def update_book_id_in_db(self, id):
        conn = sqlite3.connect(PATH_DB)
        cursor = conn.cursor()
        cursor.execute("UPDATE borrower SET book_id=? WHERE last_name=? and first_name=?",(id, self.last_name, self.first_name))
        conn.commit()
        conn.close()




    