from enum import Enum

class TextType(Enum):
    text = "plain_text"
    bold_text = "**Bold text**"
    italic_text = "_Italic text_"
    code_text = "`Code text`"
    links = "[anchor text](url)"
    images = "![alt text](url)"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url if url else None
    
    # Function to determine equality of TextNode instances
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented

        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    # Dunder method for representation, format = `TextNode(TEXT, TEXT_TYPE, URL)`
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"