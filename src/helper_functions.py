from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            new_nodes.append(node)
            continue
    
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown: Unmatched delimiter")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(split_nodes)
        
    return new_nodes

def extract_markdown_images(text: str):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    images = []
    for alt_text, url in matches:
        images.append({"alt_text": alt_text, "url": url})
    return images

def extract_markdown_links(text: str):
    pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    links = []
    for anchor_text, url in matches:
        links.append({"anchor_text": anchor_text, "url": url})
    return links

