# list_block.py
from typing import List

class Page:
    def __init__(self, page_id: int, page_entry_count: int):
        self.page_id = page_id
        self.page_entry_count = page_entry_count

    def __repr__(self) -> str:
        return f"Page(page_id={self.page_id}, page_entry_count={self.page_entry_count})"

class ListBlock:
    def __init__(self, list_size: int, list_type: str, list_id: int, filler: int, page_count: int, page_size: int,
                 page_entry_total: int, page_entry_size: int, something1: int, something2: int, something3: int,
                 something4: int, page_entry_total_2: int, something5: int, pages: List[Page]):
        self.list_size = list_size
        self.list_type = list_type
        self.list_id = list_id
        self.filler = filler
        self.page_count = page_count
        self.page_size = page_size
        self.page_entry_total = page_entry_total
        self.page_entry_size = page_entry_size
        self.something1 = something1
        self.something2 = something2
        self.something3 = something3
        self.something4 = something4
        self.page_entry_total_2 = page_entry_total_2
        self.something5 = something5
        self.pages = pages

    def __repr__(self) -> str:
        return (f"ListBlock(list_size={self.list_size}, list_type='{self.list_type}', list_id={self.list_id}, "
                f"filler={self.filler}, page_count={self.page_count}, page_size={self.page_size}, "
                f"page_entry_total={self.page_entry_total}, page_entry_size={self.page_entry_size}, "
                f"something1={self.something1}, something2={self.something2}, something3={self.something3}, "
                f"something4={self.something4}, page_entry_total_2={self.page_entry_total_2}, something5={self.something5}, "
                f"pages={self.pages})")

def create_list_block(list_size: int, page_count: int, page_size: int, page_entry_total: int,
                      page_entry_size: int, pages: List[Page]) -> ListBlock:
    """
    Creates a ListBlock instance with default values for the filler and something fields.
    """
    return ListBlock(list_size, 'LIST', -1, 0, page_count, page_size, page_entry_total, page_entry_size, 
                     2, 0, 0, 0, page_entry_total, 0, pages)

# Example usage
if __name__ == "__main__":
    pages = [Page(1, 50), Page(2, 60), Page(3, 70)]
    list_size = 100
    page_count = len(pages)
    page_size = 2048
    page_entry_total = sum(page.page_entry_count for page in pages)
    page_entry_size = 32

    list_block = create_list_block(list_size, page_count, page_size, page_entry_total, page_entry_size, pages)
    
    print(list_block)
