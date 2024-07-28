# tail_block.py
from struct import unpack

class TAILBlock:
    def __init__(self, data: bytes):
        self.data = data
        self.tail_size = None
        self.tail_type = None
        self.tail_id = None
        self.filler = None
        self.string_length = None
        self.tail_string = None

        self.parse()

    def parse(self):
        # Parse the header (16 bytes)
        header_format = '4i'
        header_size = 16
        header = unpack(header_format, self.data[:header_size])
        self.tail_size, self.tail_type, self.tail_id, self.filler = header

        # Ensure the tail type is 'TAIL'
        assert self.tail_type == 0x5441494C  # 'TAIL' in hex

        # Parse the string length (1 byte)
        offset = header_size
        self.string_length = unpack('B', self.data[offset:offset + 1])[0]
        offset += 1

        # Parse the tail string
        self.tail_string = self.data[offset:offset + self.string_length].decode('utf-8')

    def __repr__(self):
        return (f"TAILBlock(tail_size={self.tail_size}, tail_type={self.tail_type}, tail_id={self.tail_id}, "
                f"filler={self.filler}, string_length={self.string_length}, tail_string='{self.tail_string}')")

if __name__ == "__main__":
    # Example TAIL block data (this would be the actual data in a real scenario)
    example_data = (
        b'\x00\x00\x00\x20' +  # tailSize
        b'\x54\x41\x49\x4C' +  # 'TAIL'
        b'\xFF\xFF\xFF\xFF' +  # tailId (-1)
        b'\x00\x00\x00\x00' +  # filler
        b'\x13' +              # stringLength (19 for HyperCard 1.x)
        b"That's all folks..." # tail string
    )

    tail_block = TAILBlock(example_data)
    print(tail_block)
