# prst_block.py
from struct import unpack
from typing import List

class PRSTBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.page_setup_size = None
        self.page_setup_type = None
        self.page_setup_id = None
        self.filler = None
        self.printer_driver_version = None
        self.i_dev = None
        self.vert_resol = None
        self.horiz_resol = None
        self.page_top = None
        self.page_left = None
        self.page_bottom = None
        self.page_right = None
        self.paper_top = None
        self.paper_left = None
        self.paper_bottom = None
        self.paper_right = None
        self.printer_device_number = None
        self.page_v = None
        self.page_h = None
        self.port = None
        self.feed_type = None
        self.i_dev2 = None
        self.vert_resol2 = None
        self.horiz_resol2 = None
        self.page_top2 = None
        self.page_left2 = None
        self.page_bottom2 = None
        self.page_right2 = None
        self.reserved1 = None
        self.reserved2 = None
        self.reserved3 = None
        self.reserved4 = None
        self.first_page = None
        self.last_page = None
        self.num_copies = None
        self.printing_method = None
        self.reserved5 = None
        self.idle_proc = None
        self.spool_file_name = None
        self.spool_file_volume = None
        self.spool_file_version = None
        self.reserved6 = None
        self.reserved7 = None
        self.reserved8 = None
        self.reserved9 = None
        self.reserved10 = None
        self.reserved11 = None
        self.reserved12 = None
        self.reserved13 = None
        self.reserved14 = None
        self.reserved15 = None
        self.reserved16 = None
        self.reserved17 = None
        self.reserved18 = None

        self.parse()

    def parse(self):
        # Parse the initial header (16 bytes)
        header_format = '4i'
        header_size = 16
        header = unpack(header_format, self.data[:header_size])
        self.page_setup_size, self.page_setup_type, self.page_setup_id, self.filler = header
        
        # Ensure the page setup type is 'PRST'
        assert self.page_setup_type == 0x50525354  # 'PRST' in hex

        # Parse the remaining fields
        offset = header_size
        fields_format = '2h6h8h2bh6h4i3h2bi5x3i11i'
        fields = unpack(fields_format, self.data[offset:offset + 80])
        (
            self.printer_driver_version, self.i_dev, self.vert_resol, self.horiz_resol, 
            self.page_top, self.page_left, self.page_bottom, self.page_right, 
            self.paper_top, self.paper_left, self.paper_bottom, self.paper_right, 
            self.printer_device_number, self.page_v, self.page_h, self.port, 
            self.feed_type, self.i_dev2, self.vert_resol2, self.horiz_resol2, 
            self.page_top2, self.page_left2, self.page_bottom2, self.page_right2, 
            self.reserved1, self.reserved2, self.reserved3, self.reserved4, 
            self.first_page, self.last_page, self.num_copies, self.printing_method, 
            self.reserved5, self.idle_proc, self.spool_file_name, self.spool_file_volume, 
            self.spool_file_version, self.reserved6, self.reserved7, self.reserved8, 
            self.reserved9, self.reserved10, self.reserved11, self.reserved12, 
            self.reserved13, self.reserved14, self.reserved15, self.reserved16, 
            self.reserved17, self.reserved18
        ) = fields

    def __repr__(self):
        return (f"PRSTBlock(page_setup_size={self.page_setup_size}, page_setup_type={self.page_setup_type}, "
                f"page_setup_id={self.page_setup_id}, printer_driver_version={self.printer_driver_version}, "
                f"i_dev={self.i_dev}, vert_resol={self.vert_resol}, horiz_resol={self.horiz_resol}, "
                f"page_top={self.page_top}, page_left={self.page_left}, page_bottom={self.page_bottom}, "
                f"page_right={self.page_right}, paper_top={self.paper_top}, paper_left={self.paper_left}, "
                f"paper_bottom={self.paper_bottom}, paper_right={self.paper_right}, "
                f"printer_device_number={self.printer_device_number}, page_v={self.page_v}, page_h={self.page_h}, "
                f"port={self.port}, feed_type={self.feed_type}, i_dev2={self.i_dev2}, vert_resol2={self.vert_resol2}, "
                f"horiz_resol2={self.horiz_resol2}, page_top2={self.page_top2}, page_left2={self.page_left2}, "
                f"page_bottom2={self.page_bottom2}, page_right2={self.page_right2}, reserved1={self.reserved1}, "
                f"reserved2={self.reserved2}, reserved3={self.reserved3}, reserved4={self.reserved4}, "
                f"first_page={self.first_page}, last_page={self.last_page}, num_copies={self.num_copies}, "
                f"printing_method={self.printing_method}, reserved5={self.reserved5}, idle_proc={self.idle_proc}, "
                f"spool_file_name={self.spool_file_name}, spool_file_volume={self.spool_file_volume}, "
                f"spool_file_version={self.spool_file_version}, reserved6={self.reserved6}, reserved7={self.reserved7}, "
                f"reserved8={self.reserved8}, reserved9={self.reserved9}, reserved10={self.reserved10}, "
                f"reserved11={self.reserved11}, reserved12={self.reserved12}, reserved13={self.reserved13}, "
                f"reserved14={self.reserved14}, reserved15={self.reserved15}, reserved16={self.reserved16}, "
                f"reserved17={self.reserved17}, reserved18={self.reserved18})")
