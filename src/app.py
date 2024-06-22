import json
import sqlite3
import os
import logging

logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

class JSONReader:
    @staticmethod
    def read_json(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file or directory: '{file_path}'")
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return data

    @staticmethod
    def get_all_keys(entries, depth=0, max_depth=10):
        all_keys = set()
        
        for entry in entries:
            if isinstance(entry, dict):
                if depth < max_depth:
                    for key, value in entry.items():
                        all_keys.add(key)
                        if isinstance(value, (dict, list)):
                            all_keys.update(JSONReader.get_all_keys([value], depth + 1, max_depth))
            elif isinstance(entry, list):
                if depth < max_depth:
                    for item in entry:
                        if isinstance(item, (dict, list)):
                            all_keys.update(JSONReader.get_all_keys([item], depth + 1, max_depth))
        
        return all_keys

class SQLiteManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def sanitize_column_name(self, column_name):
        # Sanitize and quote column name to handle special characters
        return '"' + column_name.replace('"', '""') + '"'

    def create_table(self, table_name, columns):
        existing_columns = self.get_existing_columns(table_name)
        if not existing_columns:
            # Table does not exist, create it
            columns_def = ', '.join(self.sanitize_column_name(col) + ' TEXT' for col in columns)
            create_table_query = f'CREATE TABLE {table_name} ({columns_def})'
            self.cursor.execute(create_table_query)
        else:
            # Table exists, add missing columns
            new_columns = [col for col in columns if col not in existing_columns]
            if new_columns:
                for col in new_columns:
                    alter_table_query = f'ALTER TABLE {table_name} ADD COLUMN {self.sanitize_column_name(col)} TEXT'
                    self.cursor.execute(alter_table_query)

    def get_existing_columns(self, table_name):
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in self.cursor.fetchall()]
            return columns
        except sqlite3.Error as e:
            logging.error(f"Error getting columns from table {table_name}: {e}")
            return []

    def insert_data(self, table_name, entries, all_keys):
        self.create_table(table_name, all_keys)
        keys = ', '.join(self.sanitize_column_name(key) for key in all_keys)
        question_marks = ', '.join('?' * len(all_keys))
        insert_query = f'INSERT INTO {table_name} ({keys}) VALUES ({question_marks})'

        for entry in entries:
            if isinstance(entry, dict):
                flattened_entry = self.flatten_dict(entry)
                values = tuple(flattened_entry.get(key, None) for key in all_keys)
                self.cursor.execute(insert_query, values)

        self.connection.commit()

    @staticmethod
    def flatten_dict(d):
        def expand(key, value):
            if isinstance(value, dict):
                return [(f'{key}.{k}', v) for k, v in SQLiteManager.flatten_dict(value).items()]
            else:
                return [(key, value)] if value is not None else []

        items = [item for k, v in d.items() for item in expand(k, v)]
        return dict(items)


class DatabaseManager:
    def __init__(self, db_path):
        self.db_manager = SQLiteManager(db_path)

    def process_json_to_db(self, file_path, table_name):
        try:
            data = JSONReader.read_json(file_path)
            if isinstance(data, list):
                entries = data
            elif isinstance(data, dict):
                entries = [data]
            else:
                raise ValueError("Unsupported JSON structure")

            max_depth = 5
            all_keys = JSONReader.get_all_keys(entries, max_depth=max_depth)
            
            self.db_manager.connect()
            self.db_manager.insert_data(table_name, entries, all_keys)
            self.db_manager.close()

        except Exception as e:
            logging.error(f"Error processing JSON to DB: {e}")
            raise e

if __name__ == "__main__":
    file_path = 'nice.json'
    db_path = 'nice.db'
    table_name = 'users'

    db_manager = DatabaseManager(db_path)
    db_manager.process_json_to_db(file_path, table_name)
