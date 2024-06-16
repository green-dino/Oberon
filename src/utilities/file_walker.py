import os
import hashlib
from datetime import datetime
from prettytable import PrettyTable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class FileWalker:
    @staticmethod
    def walk(directory):
        file_info = []
        for current_root, _, file_list in os.walk(directory):
            for filename in file_list:
                full_path = os.path.join(current_root, filename)
                file_info.append(full_path)
        return file_info

class FileInformation:
    @staticmethod
    def calculate_md5(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def get_edit_date(file_path):
        return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')

    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_size(self):
        return os.path.getsize(self.file_path)

    def get_file_info(self):
        return {
            "File Size": self.get_file_size(),
            "MD5 Hash": FileInformation.calculate_md5(self.file_path),
            "Edit Date": FileInformation.get_edit_date(self.file_path)
            # Add more attributes as needed
        }

class FileInfoTable:
    def __init__(self, file_list):
        self.file_list = file_list
        self.table = PrettyTable(["File", "File Size", "MD5 Hash", "Edit Date"])
        self.table.align["File"] = 'l'

    def generate_table(self):
        for file_path in self.file_list:
            file_info = FileInformation(file_path)
            info = file_info.get_file_info()
            self.table.add_row([os.path.basename(file_path), info["File Size"], info["MD5 Hash"], info["Edit Date"]])

    def display_table(self):
        print("Files found in directory:")
        print(self.table)

def main():
    logging.info("Process started.")
    
    directory = input("Enter directory path to search: ").strip()
    if not os.path.isdir(directory):
        logging.error("Error: Invalid directory path")
        return

    file_list = FileWalker.walk(directory)
    table = FileInfoTable(file_list)
    table.generate_table()
    table.display_table()

    logging.info("Process completed.")

if __name__ == "__main__":
    main()
