from enum import Enum
from helper_functions import markdown_to_blocks, text_to_textnodes
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered list"
    ordered_list = "ordered list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.heading
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.code
    elif all(line.startswith(("- ", "* ", "+ ")) for line in lines):
        return BlockType.unordered_list
    elif lines[0].startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.paragraph
            i += 1
        return BlockType.ordered_list
    elif all(line.startswith(">") for line in lines):
        return BlockType.quote
    else:
        return BlockType.paragraph


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def heading_level(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    return level


def code_block_text(block):
    lines = block.split("\n")
    return "\n".join(lines[1:-1]) + "\n"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.heading:
            level = heading_level(block)
            html_nodes.append(
                ParentNode(
                    tag=f"h{level}",
                    children=text_to_children(block[level + 1 :].strip()),
                )
            )
        elif block_type == BlockType.code:
            html_nodes.append(
                ParentNode(
                    tag="pre",
                    children=[LeafNode(tag="code", value=code_block_text(block))],
                )
            )
        elif block_type == BlockType.quote:
            quote_text = " ".join(line.lstrip("> ").strip() for line in block.split("\n"))
            html_nodes.append(
                ParentNode(tag="blockquote", children=text_to_children(quote_text))
            )
        elif block_type == BlockType.unordered_list:
            items = [item.strip("- ").strip() for item in block.split("\n")]
            html_nodes.append(
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(tag="li", children=text_to_children(item))
                        for item in items
                    ],
                )
            )
        elif block_type == BlockType.ordered_list:
            items = [item.strip("1234567890. ").strip() for item in block.split("\n")]
            html_nodes.append(
                ParentNode(
                    tag="ol",
                    children=[
                        ParentNode(tag="li", children=text_to_children(item))
                        for item in items
                    ],
                )
            )
        else:
            paragraph = " ".join(line.strip() for line in block.split("\n"))
            html_nodes.append(ParentNode(tag="p", children=text_to_children(paragraph)))
    return ParentNode(tag="div", children=html_nodes)
