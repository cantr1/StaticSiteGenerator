from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self) -> str:
        raise NotImplementedError("to_html method must be implemented by subclasses")

    def props_to_html(self) -> str:
        """Return properties of html in a string format"""
        if not self.props:
            return ""

        props_string = ""

        for key, value in self.props.items():
            props_string += f' {key}="{value}"'
        
        return props_string

    def __repr__(self):
        return f"HTMLNode - tag: {self.tag}, value: {self.value}" \
               f", children: {self.children}, props: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode requires value")

        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return self.value

    def __repr__(self):
        return f"HTMLNode - tag: {self.tag}, value: {self.value} props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires tag")

        if not self.children:
            raise ValueError("ParentNode requires children")
        
        children_html = "".join([child.to_html() for child in self.children])

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode instance")

    if not isinstance(text_node.text_type, TextType):
        raise Exception("TextNode has invalid text type")

    if text_node.text_type == TextType.text:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.bold_text:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.italic_text:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.code_text:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.links:
        if not text_node.url:
            raise ValueError("TextNode of type links requires a url")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.images:
        if not text_node.url:
            raise ValueError("TextNode of type images requires a url")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        