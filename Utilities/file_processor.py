import os
import time
from binascii import hexlify
import hashlib
import mimetypes
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_size = self._get_file_size(file_path)
        self.mac_times = self.get_mac_times(file_path)
        self.owner = self._get_owner(file_path)
        self.mode = self._get_mode(file_path)
        self.file_header = None
        self.file_hash = None
        self.file_type = self._get_file_type(file_path)
        self.hash_type = 'sha256'

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def _get_file_size(file_path):
        return os.path.getsize(file_path)

    @staticmethod
    def get_mac_times(file_path):
        return os.path.getmtime(file_path), os.path.getctime(file_path), os.path.getatime(file_path)

    @staticmethod
    def _get_owner(file_path):
        return os.stat(file_path).st_uid

    @staticmethod
    def _get_mode(file_path):
        return os.stat(file_path).st_mode

    @staticmethod
    def _get_file_type(file_path):
        return mimetypes.guess_type(file_path)[0]

    def get_file_header(self):
        with open(self.file_path, 'rb') as file:
            self.file_header = file.read(20)

    def update_file_hash(self, hash_type='sha256'):
        self.hash_type = hash_type
        hash_func = hashlib.new(hash_type)
        with open(self.file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_func.update(chunk)
        self.file_hash = hash_func.hexdigest()

    def print_file_details(self):
        logging.info(f"File Path: {self.file_path}")
        logging.info(f"File Size: {self.file_size} bytes")
        logging.info(f"MAC Times (Modified, Accessed, Created): {tuple(time.ctime(t) for t in self.mac_times)}")
        logging.info(f"Owner (UID): {self.owner}")
        logging.info(f"Mode: {oct(self.mode)}")
        logging.info(f"File Type (MIME): {self.file_type}")
        if self.file_header:
            logging.info(f"Header (hex representation): {hexlify(self.file_header).decode()}")
        else:
            logging.info("Header: (not yet extracted)")
        if self.file_hash:
            logging.info(f"File Hash ({self.hash_type}): {self.file_hash}")
        else:
            logging.info("File Hash: (not yet computed)")

def process_directory(dir_path):
    filenames = os.listdir(dir_path)
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            try:
                if FileProcessor.file_exists(file_path):
                    file_processor = FileProcessor(file_path)
                    file_processor.get_file_header()
                    file_processor.update_file_hash()
                    file_processor.print_file_details()
                    logging.info("=" * 50)  # Separator between files
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")

def main():
    while True:
        dir_path = input("Enter a Directory to Scan or Q to Quit: ")
        if dir_path.lower() == 'q':
            break
        
        if isinstance(dir_path, str) and os.path.isdir(dir_path):
            process_directory(dir_path)
        else:
            logging.warning(f"Directory '{dir_path}' does not exist. Please enter a valid directory.")

if __name__ == "__main__":
    main()
