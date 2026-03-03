import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
db_path = os.getenv("SQLITE_PATH")


connection = sqlite3.connect(db_path)
cursor = connection.cursor()

create_table_wydatki = """CREATE TABLE wydatki 
                            (id_wydatku INTEGER PRIMARY KEY AUTOINCREMENT,
                             data TEXT,
                             tytul_operacji TEXT,
                             odbiorca TEXT,
                             id_kategorii INTEGER,
                             kwota REAL,
                             FOREIGN KEY (id_kategorii) REFERENCES kategorie (id_kategorii)) """

create_table_kategorie = """CREATE TABLE kategorie (
                                id_kategorii INTEGER PRIMARY KEY AUTOINCREMENT,
                                nazwa_kategorii TEXT) """


cursor.execute(create_table_kategorie)
cursor.execute(create_table_wydatki)
connection.commit()

