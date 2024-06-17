import os                           # File system library
import time                         # Time Conversion Library
from binascii import hexlify        # hexlify module
import hashlib                      # Hashing module
import mimetypes                    # MIME type detection module
import logging                      # Logging module

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileProcessor:
    ''' FileProcessor Class Definition '''
    def __init__(self, file_path):
        ''' Class Constructor '''
        self.file_path = file_path
        self.file_size = self._get_file_size(file_path)
        self.mac_times = self._get_mac_times(file_path)
        self.owner = self._get_owner(file_path)
        self.mode = self._get_mode(file_path)
        self.file_header = None
        self.file_hash = None
        self.file_type = self._get_file_type(file_path)
        self.hash_type = 'sha256'  # Default hash type

    @staticmethod
    def file_exists(file_path):
        ''' Verify the file exists '''
        return os.path.exists(file_path)

    @staticmethod
    def _get_file_size(file_path):
        ''' Get the size of the file '''
        return os.path.getsize(file_path)

    @staticmethod
    def _get_mac_times(file_path):
        ''' Get the MAC times (Modified, Accessed, Created) of the file '''
        return os.path.getmtime(file_path), os.path.getctime(file_path), os.path.getatime(file_path)

    @staticmethod
    def _get_owner(file_path):
        ''' Get the owner (UID) of the file '''
        return os.stat(file_path).st_uid

    @staticmethod
    def _get_mode(file_path):
        ''' Get the mode of the file '''
        return os.stat(file_path).st_mode

    @staticmethod
    def _get_file_type(file_path):
        ''' Get the MIME type of the file '''
        return mimetypes.guess_type(file_path)[0]

    def get_file_header(self):
        ''' Extract the first 20 bytes of the file header '''
        with open(self.file_path, 'rb') as file:
            self.file_header = file.read(20)

    def compute_file_hash(self, hash_type='sha256'):
        ''' Compute the hash of the file '''
        self.hash_type = hash_type
        hash_func = hashlib.new(hash_type)
        with open(self.file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_func.update(chunk)
        self.file_hash = hash_func.hexdigest()

    def print_file_details(self):
        ''' Print the metadata and print the hex representation of the header'''
        print("File Path:", self.file_path)
        print("File Size:", self.file_size, "bytes")
        print("MAC Times (Modified, Accessed, Created):", tuple(time.ctime(t) for t in self.mac_times))
        print("Owner (UID):", self.owner)
        print("Mode:", oct(self.mode))
        print("File Type (MIME):", self.file_type)
        if self.file_header:
            print("Header (hex representation):", hexlify(self.file_header).decode())
        else:
            print("Header: (not yet extracted)")
        if self.file_hash:
            print(f"File Hash ({self.hash_type}):", self.file_hash)
        else:
            print("File Hash: (not yet computed)")

def process_directory(dir_path):
    ''' Process files within a directory '''
    filenames = os.listdir(dir_path)
    for filename in filenames:
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            try:
                if FileProcessor.file_exists(file_path):
                    file_processor = FileProcessor(file_path)
                    file_processor.get_file_header()
                    file_processor.compute_file_hash()
                    file_processor.print_file_details()
                    print("=" * 50)  # Separator between files
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")

def main():
    ''' Main function '''
    while True:
        dir_path = input("Enter a Directory to Scan or Q to Quit: ")
        if dir_path.lower() == 'q':
            break
        
        if os.path.isdir(dir_path):
            process_directory(dir_path)
        else:
            print(f"Directory '{dir_path}' does not exist. Please enter a valid directory.")

if __name__ == "__main__":
    main()
