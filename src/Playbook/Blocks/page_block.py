# page_block.py
from typing import List

class PageEntry:
    def __init__(self, card_id: int, data: bytes):
        self.card_id = card_id
        self.data = data

    def __repr__(self) -> str:
        return f"PageEntry(card_id={self.card_id}, data={self.data})"

    def is_marked(self) -> bool:
        """
        Check if the card is marked based on Bit 4 of the first byte of the data.
        """
        return bool(self.data[0] & 0x10)

class PageBlock:
    def __init__(self, page_size: int, page_type: str, page_id: int, filler: int, list_id: int, something: int,
                 page_entries: List[PageEntry]):
        self.page_size = page_size
        self.page_type = page_type
        self.page_id = page_id
        self.filler = filler
        self.list_id = list_id
        self.something = something
        self.page_entries = page_entries

    def __repr__(self) -> str:
        return (f"PageBlock(page_size={self.page_size}, page_type='{self.page_type}', page_id={self.page_id}, "
                f"filler={self.filler}, list_id={self.list_id}, something={self.something}, "
                f"page_entries={self.page_entries})")

def create_page_block(page_size: int, page_id: int, list_id: int, something: int, page_entries: List[PageEntry]) -> PageBlock:
    """
    Creates a PageBlock instance with default values for the filler field.
    """
    return PageBlock(page_size, 'PAGE', page_id, 0, list_id, something, page_entries)

# Example usage
if __name__ == "__main__":
    page_entries = [PageEntry(1, bytes([0x10, 0x00, 0x00, 0x00])), PageEntry(2, bytes([0x00, 0x00, 0x00, 0x00]))]
    page_size = 2048
    page_id = 1
    list_id = 100
    something = 0

    page_block = create_page_block(page_size, page_id, list_id, something, page_entries)
    
    print(page_block)
    for entry in page_entries:
        print(f"Card ID: {entry.card_id}, Is Marked: {entry.is_marked()}")
