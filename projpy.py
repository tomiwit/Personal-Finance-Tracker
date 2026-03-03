import sqlite3
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(override=True)
db_path = os.getenv("SQLITE_PATH")
raw_path_data = os.getenv("CSV_FOLDER")

if raw_path_data:
    csv_path = Path(raw_path_data)
    print("sciezka pliku csv pobrana prawidlowo!")
else:
    print("brak pliku csv!")
    
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

columns_raw_data = [
    'Data operacji', 'Data ksiegowania', 'Tytul operacji', 
    'Dane strony operacji', 'Rachunek strony operacji', 
    'Kwota', 'Saldo', 'Waluta', 'Inne'
]
cursor.execute(create_table_kategorie)
cursor.execute(create_table_wydatki)
connection.commit()

raw_data = pd.read_csv(
    csv_path,
    skiprows=1,      
    header=None,    
    sep=',',        
    encoding='utf-8' 
)

raw_data.columns = columns_raw_data
