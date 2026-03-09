import sqlite3
import os
import pandas as pd
import random
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import json

def get_transaction_data(client, raw_text):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        config = genai.types.GenerateContentConfig(
            system_instruction="""Jesteś asystentem do analizy wydatków bankowych.
            Twoim zadaniem jest najpierw odczytanie z tytułu operacji odbiory (np zabka, kaufland, szpital carolina),
            a następnie dopasowanie kategorii.
            Na wejściu dostajesz tytuł operacji bankowej.
            Odpowiadasz TYLKO w formacie JSON, na wyjsciu oczekuję:
            {"odbiorca": "nazwa", "kategoria": "kategoria"}
            Kategorie to: jedzenie, transport, rozrywka, zdrowie, mieszkanie, ubrania, inne, blik (uzywaj tego w przypadku przelewu na telefon) ."""),
            contents = raw_text)
    clean = response.text.strip().replace("```json", "").replace("```", "").strip()
    
    result = json.loads(clean)
    return result["odbiorca"], result["kategoria"]
     

def create_tables(cursor):
    cursor.execute( """CREATE TABLE IF NOT EXISTS wydatki 
                                (id_wydatku INTEGER PRIMARY KEY AUTOINCREMENT,
                                 data TEXT,
                                 tytul_operacji TEXT,
                                 odbiorca TEXT,
                                 id_kategorii INTEGER,
                                 kwota REAL,
                                 FOREIGN KEY (id_kategorii) REFERENCES kategorie (id_kategorii)) """)
                                
    cursor.execute("""CREATE TABLE IF NOT EXISTS kategorie (
                                    id_kategorii INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nazwa_kategorii TEXT) """)



load_dotenv(override=True)
db_path = os.getenv("SQLITE_PATH")
raw_path_data = os.getenv("CSV_FOLDER")
google_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=google_api_key)


if raw_path_data:
    csv_path = Path(raw_path_data)
    print("sciezka pliku csv pobrana prawidlowo!")
else:
    print("brak pliku csv!")
    
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
create_tables(cursor)
connection.commit()


columns_raw_data = [
    'Data operacji', 'Data ksiegowania', 'Tytul operacji', 
    'Dane strony operacji', 'Rachunek strony operacji', 
    'Kwota', 'Saldo', 'Waluta', 'Inne'
]



raw_data = pd.read_csv(
    csv_path,
    skiprows=1,      
    header=None,    
    sep=',',        
    encoding='utf-8' 
)

raw_data.columns = columns_raw_data

sample = raw_data['Tytul operacji'].sample(10,random_state = 42)

for tytul in sample:
    print(f"Nazwa operacji: {tytul}")
    odbiorca_test, kategoria_test  = get_transaction_data(client, tytul)
    print(f"Odbiorca: {odbiorca_test} ||| Kategoria: {kategoria_test}\n")
    
    
for index,row in raw_data.iterrows():
    odbiorca, kategoria = get_transaction_data(client, row['Tytul operacji'])
    cursor.execute("SELECT id_kategorii, nazwa_kategorii from kategorie where nazwa_kategorii = (?)",(kategoria,))
    result = cursor.fetchone()
    if result:
        id_kat = result[0]
    else:
        cursor.execute("INSERT INTO kategorie (nazwa_kategorii) VALUES (?)", (kategoria,))
        connection.commit()
        cursor.execute("SELECT id_kategorii FROM kategorie order by id_kategorii DESC LIMIT 1")
        result = cursor.fetchone()
        id_kat = result[0]
    cursor.execute("INSERT INTO wydatki (data,tytul_operacji,odbiorca,id_kategorii,kwota) VALUES (?,?,?,?,?)",
                   (row['Data ksiegowania'],row['Tytul operacji'],odbiorca,id_kat,row['Kwota'], ))
    connection.commit()
        
