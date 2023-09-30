import sqlite3
from pathlib import Path

PATH_DB = Path.cwd() / "data/books.db"

def create_db():
    conn = sqlite3.connect(PATH_DB)
    cursor= conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                       id INTEGER PRIMARY key AUTOINCREMENT,
                       title TEXT,
                       author TEXT,
                       publication_date INTEGER,
                       borrower_id INTEGER REFERENCCES artist
                       
        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS borrower(
                       id INTEGER PRIMARY key AUTOINCREMENT,
                       last_name TEXT,
                       first_name TEXT,
                       birth_date INTEGER,
                       book_id INTEGER REFERENCCES book                      
        )""")
    conn.commit()
    conn.close()





