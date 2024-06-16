import re
from prettytable import PrettyTable

class DataProcessor:
    CHUNK_SIZE = 1024 * 1024
    OVERLAP_SIZE = 60

    ePatt = re.compile(b'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}')
    wPatt = re.compile(b'[a-zA-Z]{5,15}')
    uPatt = re.compile(b'\w+:\/\/[\w@][\w.:@]+\/?[\w.\.?=%&=\-@$,]*')

    def __init__(self, filename):
        self.filename = filename
        self.emailDict = {}
        self.urlDict = {}
        self.wordDict = {}
        self.overlapData = b""

    def process_data(self):
        try:
            with open(self.filename, 'rb') as binaryFile:
                chunkCnt = 0
                while True:
                    chunk = self.read_chunk(binaryFile)
                    if not chunk:
                        break
                    
                    self.process_chunk(chunk)

                    chunkCnt += 1
                    print(f"Processed: {chunkCnt} MB")
        except FileNotFoundError:
            print(f"File {self.filename} not found.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")

    def read_chunk(self, binaryFile):
        chunk = binaryFile.read(self.CHUNK_SIZE)
        if chunk:
            chunk = self.overlapData + chunk
            self.overlapData = chunk[-self.OVERLAP_SIZE:]
        return chunk

    def process_chunk(self, chunk):
        emails = self.ePatt.findall(chunk)
        urls = self.uPatt.findall(chunk)
        words = self.wPatt.findall(chunk)

        self._update_dict(self.emailDict, emails)
        self._update_dict(self.urlDict, urls)
        self._update_dict(self.wordDict, words)

    @staticmethod
    def _update_dict(dictionary, items):
        for item in items:
            item = item.lower()
            dictionary[item] = dictionary.get(item, 0) + 1

    def generate_tables(self):
        email_table = self.create_table(self.emailDict, 'Occurrences', 'E-Mail Address')
        url_table = self.create_table(self.urlDict, 'Occurrences', 'URLs')
        word_table = self.create_table(self.wordDict, 'Occurrences', 'Possible Words')
        return email_table, url_table, word_table

    @staticmethod
    def create_table(data_dict, column1_name, column2_name):
        table = PrettyTable([column1_name, column2_name])
        for key, value in data_dict.items():
            table.add_row([value, key.decode("ascii", "ignore")])
        return table

def display_menu():
    menu = (
        "Select an option:\n"
        "1. Display emails sorted by occurrence\n"
        "2. Display emails sorted alphabetically\n"
        "3. Display URLs sorted by occurrence\n"
        "4. Display URLs sorted alphabetically\n"
        "5. Display possible words sorted by occurrence\n"
        "6. Display possible words sorted alphabetically\n"
        "7. Exit"
    )
    print(menu)

def handle_user_choice(choice, email_table, url_table, word_table):
    if choice == '1':
        display_sorted_table(email_table, "EMAILS: Sorted by occurrence", "Occurrences", True)
    elif choice == '2':
        display_sorted_table(email_table, "EMAILS: Sorted alphabetically", "E-Mail Address")
    elif choice == '3':
        display_sorted_table(url_table, "URLs: Sorted by occurrence", "Occurrences", True)
    elif choice == '4':
        display_sorted_table(url_table, "URLs: Sorted alphabetically", "URLs")
    elif choice == '5':
        display_sorted_table(word_table, "Possible Words: Sorted by occurrence", "Occurrences", True)
    elif choice == '6':
        display_sorted_table(word_table, "Possible Words: Sorted alphabetically", "Possible Words")
    elif choice == '7':
        print("Exiting the program...")
        return False
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")
    return True

def display_sorted_table(table, title, sortby, reversesort=False):
    print(title)
    table.align = "l"
    print(table.get_string(sortby=sortby, reversesort=reversesort))

def main():
    filename = input("Enter the filename to process: ")
    processor = DataProcessor(filename)
    processor.process_data()

    email_table, url_table, word_table = processor.generate_tables()

    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if not handle_user_choice(choice, email_table, url_table, word_table):
            break

if __name__ == "__main__":
    main()
