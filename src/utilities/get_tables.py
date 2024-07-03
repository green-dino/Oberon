import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parents[1] / 'database.db'

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    return conn

# List all tables and their corresponding primary keys (if any)
conn = get_db_connection()
cursor = conn.cursor()

# Fetch all table names
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

# Define the number of rows to display per table
row_limit = 5

print("Tables:")
for table in tables:
    table_name = table[0]
    print(f"\n{table_name}:\n")
    
    # Fetch the top rows from the current table
    rows = cursor.execute(f"SELECT * FROM {table_name} LIMIT {row_limit}").fetchall()
    
    # Print the fetched rows
    for row in rows:
        print(row)

    # Indicate if there are more rows in the table
    if len(rows) == row_limit:
        print("... more rows available ...")
        
conn.close()