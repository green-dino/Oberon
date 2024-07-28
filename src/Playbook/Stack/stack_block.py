from Blocks import blocks

class StackBlock(blocks):
    def __init__(self, block_size, block_type, block_id, num_cards, id_of_one_card, list_block_id, user_level, flags, num_version_entries, card_height, card_width, patterns, script):
        super().__init__(block_size, block_type, block_id)
        self.num_cards = num_cards
        self.id_of_one_card = id_of_one_card
        self.list_block_id = list_block_id
        self.user_level = user_level
        self.flags = flags
        self.num_version_entries = num_version_entries
        self.card_height = card_height
        self.card_width = card_width
        self.patterns = patterns
        self.script = script

