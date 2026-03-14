import sqlite3

conn = sqlite3.connect("database/northwind.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

print("Tables in the database:\n")

for table in tables:
    print(table[0])