# prft_block.py
from struct import unpack
from typing import List

class PRFTBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.template_size = None
        self.template_type = None
        self.template_id = None
        self.filler = None
        self.units = None
        self.something = None
        self.margin_top = None
        self.margin_left = None
        self.margin_bottom = None
        self.margin_right = None
        self.spacing_height = None
        self.spacing_width = None
        self.cell_height = None
        self.cell_width = None
        self.flags = None
        self.header_length = None
        self.header = None
        self.report_item_count = None
        self.report_items = []

        self.parse()

    def parse(self):
        # Parse the initial header (16 bytes)
        header_format = '4i'
        header_size = 16
        header = unpack(header_format, self.data[:header_size])
        self.template_size, self.template_type, self.template_id, self.filler = header

        # Ensure the template type is 'PRFT'
        assert self.template_type == 0x50524654  # 'PRFT' in hex

        # Parse the remaining fields
        offset = header_size
        main_fields_format = '2b8h2b'
        main_fields_size = 20
        (
            self.units, self.something, self.margin_top, self.margin_left,
            self.margin_bottom, self.margin_right, self.spacing_height,
            self.spacing_width, self.cell_height, self.cell_width,
            self.flags, self.header_length
        ) = unpack(main_fields_format, self.data[offset:offset + main_fields_size])
        offset += main_fields_size

        # Parse the header string
        self.header = self.data[offset:offset + self.header_length].decode('utf-8')
        offset += self.header_length

        # Skip to offset 0x0124 (292 bytes)
        offset = 0x0124

        # Parse the report items
        self.report_item_count = unpack('h', self.data[offset:offset + 2])[0]
        offset += 2

        report_item_format = '8h2bhh'
        report_item_size = 24

        for _ in range(self.report_item_count):
            report_item_data = self.data[offset:offset + report_item_size]
            report_item = unpack(report_item_format, report_item_data)
            (
                report_item_size, top, left, bottom, right, column_count,
                flags, text_size, text_height, text_style, reserved, text_align
            ) = report_item

            offset += report_item_size

            # Parse the contents and textFont
            contents, text_font = '', ''
            while self.data[offset] != 0:
                contents += chr(self.data[offset])
                offset += 1
            offset += 1  # Skip the null terminator

            while self.data[offset] != 0:
                text_font += chr(self.data[offset])
                offset += 1
            offset += 1  # Skip the null terminator

            self.report_items.append({
                'report_item_size': report_item_size,
                'top': top,
                'left': left,
                'bottom': bottom,
                'right': right,
                'column_count': column_count,
                'flags': flags,
                'text_size': text_size,
                'text_height': text_height,
                'text_style': text_style,
                'reserved': reserved,
                'text_align': text_align,
                'contents': contents,
                'text_font': text_font
            })

    def __repr__(self):
        report_items_str = ', '.join([str(item) for item in self.report_items])
        return (f"PRFTBlock(template_size={self.template_size}, template_type={self.template_type}, "
                f"template_id={self.template_id}, units={self.units}, something={self.something}, "
                f"margin_top={self.margin_top}, margin_left={self.margin_left}, margin_bottom={self.margin_bottom}, "
                f"margin_right={self.margin_right}, spacing_height={self.spacing_height}, "
                f"spacing_width={self.spacing_width}, cell_height={self.cell_height}, cell_width={self.cell_width}, "
                f"flags={self.flags}, header_length={self.header_length}, header='{self.header}', "
                f"report_item_count={self.report_item_count}, report_items=[{report_items_str}])")
