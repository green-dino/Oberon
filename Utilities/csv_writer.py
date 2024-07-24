import csv
import logging

# Initialize logger
log = logging.getLogger(__name__)

class CSVFileHandler:
    """Handles opening, writing, and closing of CSV files."""
    
    @staticmethod
    def initialize_csv_file(file_name, hash_type):
        """Initializes a new CSV file with headers."""
        try:
            with open(file_name, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writerow(['File', 'Path', 'Size', 'Modified Time', 'Access Time',
                                  'Created Time', hash_type, 'Owner', 'Group', 'Mode'])
            return True
        except Exception as e:
            log.error(f'CSV File Initialization Failure: {e}')
            return False

class _CSVWriter:
    def __init__(self, file_name, hash_type):
        self.file_name = file_name
        self.hash_type = hash_type
        self.success = CSVFileHandler.initialize_csv_file(file_name, hash_type)

    def write_row(self, file_name, file_path, file_size, m_time, a_time, c_time, hash_val, owner, group, mode):
        """Writes a single row to the CSV file."""
        if self.success:
            with open(self.file_name, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writerow([file_name, file_path, file_size, m_time, a_time, c_time, hash_val, owner, group, mode])
        else:
            log.error('Cannot write to CSV: File initialization failed.')

    def close_writer(self):
        """Closes the CSV file."""
        if self.success:
            try:
                with open(self.file_name, 'r+') as csv_file:
                    csv_file.truncate(0)  # Clear content
                    csv_file.seek(0)      # Reset position to start
                    csv_file.close()     # Close the file
            except Exception as e:
                log.error(f'Error closing CSV file: {e}')
        else:
            log.error('Cannot close CSV: File initialization failed.')
