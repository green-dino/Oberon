# prnt_block.py
from struct import unpack
from typing import List

class Template:
    def __init__(self, template_id, template_name_length, template_name):
        self.template_id = template_id
        self.template_name_length = template_name_length
        self.template_name = template_name

    def __repr__(self):
        return f"Template(template_id={self.template_id}, template_name_length={self.template_name_length}, template_name='{self.template_name}')"


class PRNTBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.print_size = None
        self.print_type = None
        self.print_id = None
        self.filler = None
        self.page_setup_id = None
        self.template_count = None
        self.templates: List[Template] = []
        self.unknown_section_1 = None
        self.unknown_section_2 = None

        self.parse()

    def parse(self):
        # Parse the initial header (16 bytes)
        header_format = '4i'
        header_size = 16
        header = unpack(header_format, self.data[:header_size])
        self.print_size, self.print_type, self.print_id, self.filler = header
        
        # Ensure the print type is 'PRNT'
        assert self.print_type == 0x50524E54  # 'PRNT' in hex

        # Skip to offset 0x0030 (48 bytes) and parse pageSetupId
        offset = 0x0030
        self.page_setup_id = unpack('h', self.data[offset:offset + 2])[0]
        
        # Skip to offset 0x0134 (308 bytes) and parse templateCount
        offset = 0x0134
        self.template_count = unpack('h', self.data[offset:offset + 2])[0]
        offset += 2
        
        # Parse templates
        template_size = 36
        for _ in range(self.template_count):
            template_id = unpack('i', self.data[offset:offset + 4])[0]
            template_name_length = self.data[offset + 4]
            template_name = self.data[offset + 5:offset + 5 + template_name_length].decode('ascii')
            offset += template_size
            template = Template(template_id, template_name_length, template_name)
            self.templates.append(template)

    def __repr__(self):
        return (f"PRNTBlock(print_size={self.print_size}, print_type={self.print_type}, print_id={self.print_id}, "
                f"page_setup_id={self.page_setup_id}, template_count={self.template_count}, templates={self.templates})")

