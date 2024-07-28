class Part:
    def __init__(self, length, type_, flags, top, left, bottom, right, more_flags, title_width, icon_id, text_alignment, text_font_id, text_font_size, line_height, text_style_flags, name, script):
        self.length = length
        self.type = type_
        self.flags = flags
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.more_flags = more_flags
        self.title_width = title_width
        self.icon_id = icon_id
        self.text_alignment = text_alignment
        self.text_font_id = text_font_id
        self.text_font_size = text_font_size
        self.line_height = line_height
        self.text_style_flags = text_style_flags
        self.name = name
        self.script = script

class PartContent:
    def __init__(self, part_id, length, styles_length, styles_data, text_data, name, script):
        self.part_id = part_id
        self.length = length
        self.styles_length = styles_length
        self.styles_data = styles_data
        self.text_data = text_data
        self.name = name
        self.script = script
