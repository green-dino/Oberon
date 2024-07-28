# ftbl_block.py
from struct import unpack
from typing import List

class Font:
    def __init__(self, font_id, font_name, align):
        self.font_id = font_id
        self.font_name = font_name
        self.align = align

    def __repr__(self):
        return f"Font(font_id={self.font_id}, font_name='{self.font_name}', align={self.align})"


class FTBLBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.font_table_size = None
        self.font_table_type = None
        self.font_table_id = None
        self.filler = None
        self.font_count = None
        self.something = None
        self.fonts: List[Font] = []

        self.parse()

    def parse(self):
        # Header is 24 bytes long
        header_format = '6i'
        header_size = 24
        header = unpack(header_format, self.data[:header_size])
        self.font_table_size, self.font_table_type, self.font_table_id, self.filler, self.font_count, self.something = header
        
        # Ensure the font table type is 'FTBL'
        assert self.font_table_type == 0x4654424C  # 'FTBL' in hex

        # Parse fonts
        offset = header_size
        for _ in range(self.font_count):
            # Read font ID
            font_id = unpack('i', self.data[offset:offset + 4])[0]
            offset += 4
            
            # Read font name
            font_name_end = self.data.find(b'\x00', offset)  # Null-terminated string
            font_name = self.data[offset:font_name_end].decode('ascii')
            offset = font_name_end + 1  # Move past the null terminator
            
            # Read alignment
            align = unpack('h', self.data[offset:offset + 2])[0]
            offset += 2
            
            font = Font(font_id, font_name, align)
            self.fonts.append(font)

    def __repr__(self):
        return (f"FTBLBlock(font_table_size={self.font_table_size}, font_table_type={self.font_table_type}, "
                f"font_table_id={self.font_table_id}, font_count={self.font_count}, fonts={self.fonts})")
