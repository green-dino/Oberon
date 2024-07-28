import logging
from typing import List, Tuple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BMAPBlock:
    """
    A class to handle decompression of bitmap data using various opcodes.
    """

    def __init__(self, bounding_rect: Tuple[int, int, int, int], compressed_data: bytes, mask_data: bytes = None):
        """
        Initialize the BMAPBlock with bounding rectangle and compressed data.
        """
        self.bounding_rect = bounding_rect
        self.compressed_data = compressed_data
        self.mask_data = mask_data
        self.decompressed_data = bytearray()
        self.dh = 0
        self.dv = 0
        self.prev_rows = []

    def decompress(self):
        left, top, right, bottom = self.bounding_rect
        row_length = ((right - left + 31) // 32) * 32  # Adjust to the nearest multiple of 32

        i = 0
        valid_opcodes = set(range(0x00, 0x90)).union(range(0xA0, 0xE0), range(0xE0, 0x100))
        
        while i < len(self.compressed_data):
            opcode = self.compressed_data[i]
            i += 1

            if opcode not in valid_opcodes:
                raise ValueError(f"Invalid opcode {opcode} at position {i-1}")
            
            logger.debug(f"Processing opcode {opcode} at index {i-1}")

            if 0x00 <= opcode <= 0x7F:
                z = opcode >> 4
                d = opcode & 0x0F
                self.decompressed_data.extend([0] * z)
                self.decompressed_data.extend(self.compressed_data[i:i + d])
                i += d

            elif opcode == 0x80:
                self.decompressed_data.extend(self.compressed_data[i:i + row_length])
                i += row_length

            elif opcode == 0x81:
                self.decompressed_data.extend([0xFF] * row_length)

            elif opcode == 0x82:
                self.decompressed_data.extend([0x00] * row_length)

            elif opcode == 0x83:
                byte = self.compressed_data[i]
                self.decompressed_data.extend([byte] * row_length)
                self.prev_rows.append(byte)
                if len(self.prev_rows) > 8:
                    self.prev_rows.pop(0)
                i += 1

            elif opcode == 0x84:
                row_num = len(self.decompressed_data) // row_length
                byte = self.prev_rows[row_num % 8]
                self.decompressed_data.extend([byte] * row_length)

            elif opcode == 0x85:
                self.decompressed_data.extend(self.decompressed_data[-row_length:])

            elif opcode == 0x86:
                self.decompressed_data.extend(self.decompressed_data[-2 * row_length:-row_length])

            elif opcode == 0x87:
                self.decompressed_data.extend(self.decompressed_data[-3 * row_length:-2 * row_length])

            elif 0x88 <= opcode <= 0x8F:
                self.update_dh_dv(opcode)

            elif 0xA0 <= opcode <= 0xBF:
                repeat_count = opcode & 0x1F
                next_opcode = self.compressed_data[i]
                i += 1
                for _ in range(repeat_count):
                    self.process_opcode(next_opcode, i, row_length)

            elif 0xC0 <= opcode <= 0xDF:
                d = opcode & 0x1F
                self.decompressed_data.extend(self.compressed_data[i:i + d * 8])
                i += d * 8

            elif 0xE0 <= opcode <= 0xFF:
                z = opcode & 0x1F
                self.decompressed_data.extend([0x00] * (z * 16))

            if len(self.decompressed_data) >= row_length * (bottom - top):
                break
            
            if len(self.decompressed_data) % (row_length * 100) == 0:
                print(f"Decompressed {len(self.decompressed_data)} bytes so far...")

    def update_dh_dv(self, opcode):
        """
        Update dh and dv values based on the opcode.
        """
        if opcode == 0x88:
            self.dh, self.dv = 16, 0
        elif opcode == 0x89:
            self.dh, self.dv = 0, 0
        elif opcode == 0x8A:
            self.dh, self.dv = 0, 1
        elif opcode == 0x8B:
            self.dh, self.dv = 0, 2
        elif opcode == 0x8C:
            self.dh, self.dv = 1, 0
        elif opcode == 0x8D:
            self.dh, self.dv = 1, 1
        elif opcode == 0x8E:
            self.dh, self.dv = 2, 2
        elif opcode == 0x8F:
            self.dh, self.dv = 8, 0

    def process_opcode(self, opcode, i, row_length):
        """
        Process an individual opcode.
        """
        if 0x00 <= opcode <= 0x7F:
            z = opcode >> 4
            d = opcode & 0x0F
            self.decompressed_data.extend([0] * z)
            self.decompressed_data.extend(self.compressed_data[i:i + d])
        elif opcode == 0x80:
            self.decompressed_data.extend(self.compressed_data[i:i + row_length])
        elif opcode == 0x81:
            self.decompressed_data.extend([0xFF] * row_length)
        elif opcode == 0x82:
            self.decompressed_data.extend([0x00] * row_length)
        elif opcode == 0x83:
            byte = self.compressed_data[i]
            self.decompressed_data.extend([byte] * row_length)
            self.prev_rows.append(byte)
            if len(self.prev_rows) > 8:
                self.prev_rows.pop(0)
       
