from struct import unpack
from typing import List
from enum import IntEnum

# Define constants and enums
FONT_TABLE_TYPE_FTBL = 0x4654424C  # 'FTBL' in hex
HEADER_SIZE = 24
FONT_ID_SIZE = 4
FONT_NAME_TERMINATOR = b"\x00"
FONT_ALIGN_SIZE = 2


class FontTableType(IntEnum):
    """Enumeration for font table types."""

    FTBL = FONT_TABLE_TYPE_FTBL


class Font:
    """
    Represents a font entry in the FTBL block.

    Attributes:
        font_id (int): The ID of the font.
        font_name (str): The name of the font.
        align (int): The alignment value of the font.
    """

    def __init__(self, font_id: int, font_name: str, align: int):
        """
        Initializes a new Font instance.

        Args:
            font_id (int): The ID of the font.
            font_name (str): The name of the font.
            align (int): The alignment value of the font.
        """
        self.font_id = font_id
        self.font_name = font_name
        self.align = align

    def __repr__(self) -> str:
        """
        Returns a string representation of the Font instance.

        Returns:
            str: String representation of the Font.
        """
        return f"Font(font_id={self.font_id}, font_name='{self.font_name}', align={self.align})"


class FTBLBlock:
    """
    Represents an FTBL block which contains font information.

    Attributes:
        data (bytes): The raw binary data of the FTBL block.
        font_table_size (int): The size of the font table.
        font_table_type (int): The type of the font table.
        font_table_id (int): The ID of the font table.
        filler (int): Filler data in the header.
        font_count (int): The number of fonts in the table.
        something (int): Placeholder for an unknown value in the header.
        fonts (List[Font]): List of Font objects parsed from the data.
    """

    def __init__(self, data: bytes):
        """
        Initializes a new FTBLBlock instance and parses the data.

        Args:
            data (bytes): The raw binary data of the FTBL block.
        """
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
        """
        Parses the binary data to extract the font table header and font entries.

        Raises:
            ValueError: If the font table type is invalid.
        """
        # Parsing method
        header = unpack("6i", self.data[:HEADER_SIZE])
        (
            self.font_table_size,
            self.font_table_type,
            self.font_table_id,
            self.filler,
            self.font_count,
            self.something,
        ) = header

        # Error handling
        if self.font_table_type != FontTableType.FTBL:
            raise ValueError("Invalid font table type")

        # Parse fonts
        offset = HEADER_SIZE
        for _ in range(self.font_count):
            font_id = unpack("i", self.data[offset : offset + FONT_ID_SIZE])[0]
            offset += FONT_ID_SIZE

            font_name_end = self.data.find(FONT_NAME_TERMINATOR, offset)
            font_name = self.data[offset:font_name_end].decode("ascii")
            offset = font_name_end + 1

            align = unpack("h", self.data[offset : offset + FONT_ALIGN_SIZE])[0]
            offset += FONT_ALIGN_SIZE

            font = Font(font_id, font_name, align)
            self.fonts.append(font)

    def __repr__(self) -> str:
        """
        Returns a string representation of the FTBLBlock instance.

        Returns:
            str: String representation of the FTBLBlock.
        """
        return (
            f"FTBLBlock(font_table_size={self.font_table_size}, font_table_type={self.font_table_type}, "
            f"font_table_id={self.font_table_id}, font_count={self.font_count}, fonts={self.fonts})"
        )
