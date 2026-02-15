import sqlite3
import os

DATABASE = "data/database.db"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
''')

conn.commit()
conn.close()

print("Database initialized successfully.")
