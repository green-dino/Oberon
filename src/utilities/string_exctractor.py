import re
from collections import Counter

class StringExtractor:
    WORD_PATTERN = re.compile(b'[a-zA-Z]{5,15}')
    
    @staticmethod
    def extract_strings_from_binary(data):
        """Extracts words of length 5 to 15 characters from binary data."""
        return StringExtractor.WORD_PATTERN.findall(data)
    
class StringCounter:
    @staticmethod
    def count_unique_strings(data_chunks):
        """Counts unique strings from an iterable of binary data chunks."""
        occurrences = Counter()
        for chunk in data_chunks:
            strings = StringExtractor.extract_strings_from_binary(chunk)
            occurrences.update(strings)
        return occurrences
