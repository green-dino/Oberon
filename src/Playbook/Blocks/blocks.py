from collections import deque

class Block:
    def __init__(self, block_size, block_type, block_id, data):
        self.block_size = block_size
        self.block_type = block_type
        self.block_id = block_id
        self.data = data
    
    def __repr__(self) -> str:
        pass

