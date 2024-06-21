import json
import sqlite3
import os

class DatabaseManager:

    @staticmethod
    def read_json(file_path):
        """Read the JSON file and return its content."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return data

    @staticmethod
    def get_all_keys(entries):
        """Identify all unique keys from the JSON data entries."""
        all_keys = set()
        for entry in entries:
            all_keys.update(entry.keys())
        return all_keys

    @staticmethod
    def create_table(cursor, table_name, columns):
        """Create a table in the SQLite3 database."""
        columns_def = ', '.join(f'"{col}" TEXT' for col in columns)
        create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})'
        cursor.execute(create_table_query)

    @staticmethod
    def insert_data(cursor, table_name, entries, all_keys):
        """Insert data into the SQLite3 database."""
        keys = ', '.join(f'"{key}"' for key in all_keys)
        question_marks = ', '.join('?' * len(all_keys))

        for entry in entries:
            values = tuple(entry.get(key, None) for key in all_keys)
            insert_query = f'INSERT INTO {table_name} ({keys}) VALUES ({question_marks})'
            
            try:
                cursor.execute(insert_query, values)
            except sqlite3.ProgrammingError as e:
                print(f"Error inserting data: {e}")
                print(f"Entry: {entry}")
                print(f"Values: {values}")

    @staticmethod
    def process_json_to_db(file_path, db_path, table_name):
        """Main method to process JSON data and insert it into the database."""
        # Step 1: Read the JSON file
        data = DatabaseManager.read_json(file_path)

        # Handle both list and dictionary structures
        if isinstance(data, list):
            entries = data
        elif isinstance(data, dict):
            entries = [data]
        else:
            raise ValueError("Unsupported JSON structure")

        # Step 2: Identify all unique keys
        all_keys = DatabaseManager.get_all_keys(entries)

        # Step 3: Create a connection to the SQLite3 database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Step 4: Create the table
        DatabaseManager.create_table(cursor, table_name, all_keys)

        # Step 5: Insert data into the SQLite3 database
        DatabaseManager.insert_data(cursor, table_name, entries, all_keys)

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

if __name__ == "__main__":
    file_path = 'nice.json'
    db_path = 'nice.db'
    table_name = 'users'

    DatabaseManager.process_json_to_db(file_path, db_path, table_name)
