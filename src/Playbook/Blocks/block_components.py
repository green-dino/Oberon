from blocks import Block 

class StyleTableBlock(Block):
    def __init__(self, block_size, block_type, block_id, num_styles, styles):
        super().__init__(block_size, block_type, block_id)
        self.num_styles = num_styles
        self.styles = styles

class PageTableListBlock(Block):
    def __init__(self, block_size, block_type, block_id, num_page_tables, size_of_card_blocks):
        super().__init__(block_size, block_type, block_id)
        self.num_page_tables = num_page_tables
        self.size_of_card_blocks = size_of_card_blocks

class PageTableBlock(Block):
    def __init__(self, block_size, block_type, block_id, page_table_list):
        super().__init__(block_size, block_type, block_id)
        self.page_table_list = page_table_list

class CardOrBackgroundBlock(Block):
    def __init__(self, block_size, block_type, block_id, bmap_block_id, flags, background_id, num_parts, num_part_contents, script_type, parts):
        super().__init__(block_size, block_type, block_id)
        self.bmap_block_id = bmap_block_id
        self.flags = flags
        self.background_id = background_id
        self.num_parts = num_parts
        self.num_part_contents = num_part_contents
        self.script_type = script_type
        self.parts = parts


class PageTableListBlock(Block):
    def __init__(self, block_id, num_page_tables, card_block_size, page_tables):
        size = 24 + len(page_tables) * 6
        super().__init__(size, 'LIST', block_id, None)
        self.num_page_tables = num_page_tables
        self.card_block_size = card_block_size
        self.page_tables = page_tables

class PageTableBlock(Block):
    def __init__(self, block_id, card_ids, placeholder):
        size = 16 + len(card_ids) * 5
        super().__init__(size, 'PAGE', block_id, None)
        self.card_ids = card_ids
        self.placeholder = placeholder