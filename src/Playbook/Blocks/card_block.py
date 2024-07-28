# card_block.py
from typing import List

class Part:
    def __init__(self, size: int, part_id: int, part_type: int, flags: int, top: int, left: int, bottom: int, right: int, 
                 show_name: bool, hilite: bool, auto_hilite: bool, family: int, style: int, 
                 title_width: int, icon_id: int, text_align: int, text_font: int, text_size: int, 
                 text_style: int, text_height: int, name: str, part_script: str):
        self.size = size
        self.part_id = part_id
        self.part_type = part_type
        self.flags = flags
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.show_name = show_name
        self.hilite = hilite
        self.auto_hilite = auto_hilite
        self.family = family
        self.style = style
        self.title_width = title_width
        self.icon_id = icon_id
        self.text_align = text_align
        self.text_font = text_font
        self.text_size = text_size
        self.text_style = text_style
        self.text_height = text_height
        self.name = name
        self.part_script = part_script

    def __repr__(self) -> str:
        return (f"Part(size={self.size}, part_id={self.part_id}, part_type={self.part_type}, flags={self.flags}, "
                f"top={self.top}, left={self.left}, bottom={self.bottom}, right={self.right}, "
                f"show_name={self.show_name}, hilite={self.hilite}, auto_hilite={self.auto_hilite}, family={self.family}, "
                f"style={self.style}, title_width={self.title_width}, icon_id={self.icon_id}, text_align={self.text_align}, "
                f"text_font={self.text_font}, text_size={self.text_size}, text_style={self.text_style}, text_height={self.text_height}, "
                f"name='{self.name}', part_script='{self.part_script}')")

class PartContent:
    def __init__(self, part_id: int, content_size: int, content: str):
        self.part_id = part_id
        self.content_size = content_size
        self.content = content

    def __repr__(self) -> str:
        return f"PartContent(part_id={self.part_id}, content_size={self.content_size}, content='{self.content}')"

class CardBlock:
    def __init__(self, card_size: int, card_id: int, bitmap_id: int, flags: int, page_id: int, bkgnd_id: int,
                 part_count: int, part_content_count: int, parts: List[Part], part_contents: List[PartContent],
                 card_name: str, card_script: str):
        self.card_size = card_size
        self.card_type = 'CARD'
        self.card_id = card_id
        self.filler = 0
        self.bitmap_id = bitmap_id
        self.flags = flags
        self.page_id = page_id
        self.bkgnd_id = bkgnd_id
        self.part_count = part_count
        self.part_content_count = part_content_count
        self.parts = parts
        self.part_contents = part_contents
        self.card_name = card_name
        self.card_script = card_script

    def __repr__(self) -> str:
        return (f"CardBlock(card_size={self.card_size}, card_type='{self.card_type}', card_id={self.card_id}, "
                f"filler={self.filler}, bitmap_id={self.bitmap_id}, flags={self.flags}, page_id={self.page_id}, "
                f"bkgnd_id={self.bkgnd_id}, part_count={self.part_count}, part_content_count={self.part_content_count}, "
                f"parts={self.parts}, part_contents={self.part_contents}, card_name='{self.card_name}', card_script='{self.card_script}')")

def create_card_block(card_size: int, card_id: int, bitmap_id: int, flags: int, page_id: int, bkgnd_id: int,
                      parts: List[Part], part_contents: List[PartContent], card_name: str, card_script: str) -> CardBlock:
    part_count = len(parts)
    part_content_count = len(part_contents)
    return CardBlock(card_size, card_id, bitmap_id, flags, page_id, bkgnd_id,
                     part_count, part_content_count, parts, part_contents, card_name, card_script)

# Example usage
if __name__ == "__main__":
    parts = [
        Part(10, 1, 1, 0, 10, 10, 50, 50, True, False, True, 1, 0, 0, 1, 12, 0, 0, "Button1", ""),
        Part(12, 2, 2, 1, 60, 60, 100, 100, False, True, False, 2, 0, 0, 1, 14, 0, 0, "Field1", "")
    ]
    part_contents = [
        PartContent(1, 10, "Content1"),
        PartContent(2, 12, "Content2")
    ]
    card_block = create_card_block(2048, 1, 2, 0, 3, 4, parts, part_contents, "Card1", "Script1")
    
    print(card_block)
