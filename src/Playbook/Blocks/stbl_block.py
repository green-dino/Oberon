# stbl_block.py
from struct import unpack
from typing import List

class Style:
    def __init__(self, style_id, something1, something2, text_font, text_style, text_style_changed, text_size, something3, something4, something5):
        self.style_id = style_id
        self.something1 = something1
        self.something2 = something2
        self.text_font = text_font
        self.text_style = text_style
        self.text_style_changed = text_style_changed
        self.text_size = text_size
        self.something3 = something3
        self.something4 = something4
        self.something5 = something5

    def __repr__(self):
        return (f"Style(style_id={self.style_id}, text_font={self.text_font}, text_style={self.text_style}, "
                f"text_style_changed={self.text_style_changed}, text_size={self.text_size})")


class STBLBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.style_table_size = None
        self.style_table_type = None
        self.style_table_id = None
        self.filler = None
        self.style_count = None
        self.next_style_id = None
        self.styles: List[Style] = []

        self.parse()

    def parse(self):
        # Header is 24 bytes long
        header_format = '6i'
        header_size = 24
        header = unpack(header_format, self.data[:header_size])
        self.style_table_size, self.style_table_type, self.style_table_id, self.filler, self.style_count, self.next_style_id = header
        
        # Ensure the style table type is 'STBL'
        assert self.style_table_type == 0x5354424C  # 'STBL' in hex

        # Each style is 20 bytes long
        style_format = '3i2b5h'
        style_size = 20

        for i in range(self.style_count):
            offset = header_size + i * style_size
            style_data = unpack(style_format, self.data[offset:offset + style_size])
            style = Style(*style_data)
            self.styles.append(style)

    def __repr__(self):
        return (f"STBLBlock(style_table_size={self.style_table_size}, style_table_type={self.style_table_type}, "
                f"style_table_id={self.style_table_id}, style_count={self.style_count}, next_style_id={self.next_style_id}, "
                f"styles={self.styles})")


