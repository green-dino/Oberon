# blocks.py
from collections import deque
from typing import List

class BlockType:
    STAK = 'STAK'
    MAST = 'MAST'
    LIST = 'LIST'
    PAGE = 'PAGE'
    BKGD = 'BKGD'
    CARD = 'CARD'
    BMAP = 'BMAP'
    FREE = 'FREE'
    STBL = 'STBL'
    FTBL = 'FTBL'
    PRNT = 'PRNT'
    PRST = 'PRST'
    PRFT = 'PRFT'
    TAIL = 'TAIL'

class Block:
    def __init__(self, block_size: int, block_type: str, block_id: int, data: bytes):
        self.block_size = block_size
        self.block_type = block_type
        self.block_id = block_id
        self.data = data

    def __repr__(self) -> str:
        return (f"Block(block_size={self.block_size}, block_type='{self.block_type}', "
                f"block_id={self.block_id}, data_length={len(self.data)})")

class StackBlock(Block):
    def __init__(self, stack_size: int, stack_type: int, stack_id: int, format: int, total_size: int,
                 something1: int, something2: int, bkgnd_count: int, first_bkgnd_id: int, card_count: int,
                 first_card_id: int, list_id: int, free_count: int, free_size: int, print_id: int, password: int,
                 user_level: int, flags: int, create_version: int, compact_version: int, modify_version: int,
                 open_version: int, checksum: int, window_top: int, window_left: int, window_bottom: int,
                 window_right: int, screen_top: int, screen_left: int, screen_bottom: int, screen_right: int,
                 scroll_y: int, scroll_x: int, data: bytes):
        super().__init__(stack_size, BlockType.STAK, stack_id, data)
        self.stack_type = stack_type
        self.format = format
        self.total_size = total_size
        self.something1 = something1
        self.something2 = something2
        self.bkgnd_count = bkgnd_count
        self.first_bkgnd_id = first_bkgnd_id
        self.card_count = card_count
        self.first_card_id = first_card_id
        self.list_id = list_id
        self.free_count = free_count
        self.free_size = free_size
        self.print_id = print_id
        self.password = password
        self.user_level = user_level
        self.flags = flags
        self.create_version = create_version
        self.compact_version = compact_version
        self.modify_version = modify_version
        self.open_version = open_version
        self.checksum = checksum
        self.window_top = window_top
        self.window_left = window_left
        self.window_bottom = window_bottom
        self.window_right = window_right
        self.screen_top = screen_top
        self.screen_left = screen_left
        self.screen_bottom = screen_bottom
        self.screen_right = screen_right
        self.scroll_y = scroll_y
        self.scroll_x = scroll_x

    def __repr__(self) -> str:
        return (f"StackBlock(stack_size={self.block_size}, stack_type={self.stack_type}, stack_id={self.block_id}, "
                f"format={self.format}, total_size={self.total_size}, bkgnd_count={self.bkgnd_count}, "
                f"first_bkgnd_id={self.first_bkgnd_id}, card_count={self.card_count}, first_card_id={self.first_card_id}, "
                f"list_id={self.list_id}, free_count={self.free_count}, free_size={self.free_size}, print_id={self.print_id}, "
                f"password={self.password}, user_level={self.user_level}, flags={self.flags}, create_version={self.create_version}, "
                f"compact_version={self.compact_version}, modify_version={self.modify_version}, open_version={self.open_version}, "
                f"checksum={self.checksum}, window_top={self.window_top}, window_left={self.window_left}, "
                f"window_bottom={self.window_bottom}, window_right={self.window_right}, screen_top={self.screen_top}, "
                f"screen_left={self.screen_left}, screen_bottom={self.screen_bottom}, screen_right={self.screen_right}, "
                f"scroll_y={self.scroll_y}, scroll_x={self.scroll_x}, data_length={len(self.data)})")

def validate_blocks(blocks: List[Block]) -> bool:
    """
    Validate the order and constraints of the blocks.
    """
    if not blocks:
        return False

    expected_first_blocks = [BlockType.STAK, BlockType.MAST, BlockType.LIST, BlockType.PAGE]
    if not all(blocks[i].block_type == expected_first_blocks[i] for i in range(len(expected_first_blocks))):
        return False

    if blocks[-1].block_type != BlockType.TAIL:
        return False

    return True

def create_block(block_size: int, block_type: str, block_id: int, data: bytes) -> Block:
    return Block(block_size, block_type, block_id, data)
