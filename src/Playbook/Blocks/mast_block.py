# mast_block.py
from typing import List

class MastBlock:
    def __init__(self, master_size: int, master_type: str, master_id: int, filler: int, something1: int,
                 something2: int, something3: int, something4: int, address_info: List[int]):
        self.master_size = master_size
        self.master_type = master_type
        self.master_id = master_id
        self.filler = filler
        self.something1 = something1
        self.something2 = something2
        self.something3 = something3
        self.something4 = something4
        self.address_info = address_info

    def __repr__(self) -> str:
        return (f"MastBlock(master_size={self.master_size}, master_type='{self.master_type}', master_id={self.master_id}, "
                f"filler={self.filler}, something1={self.something1}, something2={self.something2}, "
                f"something3={self.something3}, something4={self.something4}, address_info={self.address_info})")

    @staticmethod
    def parse_address_info(master_size: int, address_info: List[int]) -> List[int]:
        """
        Parses the address_info field to extract block offsets and ID numbers.
        """
        parsed_info = []
        for entry in address_info:
            offset = (entry >> 8) * 32
            block_id = entry & 0xFF
            parsed_info.append((offset, block_id))
        return parsed_info

def create_mast_block(master_size: int, address_info: List[int]) -> MastBlock:
    """
    Creates a MastBlock instance with default values for the filler and something fields.
    """
    return MastBlock(master_size, 'MAST', -1, 0, 0, 0, 0, 0, address_info)