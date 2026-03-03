import sqlite3
import os
from dotenv import load_dotenv


load_dotenv()
db_path = os.getenv("SQLITE_PATH")

print(db_path)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()