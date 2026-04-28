from textnode import TextType, TextNode
import re
import textwrap

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(
                f"![{image['alt_text']}]({image['url']})", 1
            )
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.text))
            new_nodes.append(
                TextNode(
                    image["alt_text"],
                    TextType.images,
                    image["url"],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(
                f"[{link['anchor_text']}]({link['url']})", 1
            )
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.text))
            new_nodes.append(
                TextNode(link["anchor_text"], TextType.links, link["url"])
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.text))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold_text)
    nodes = split_nodes_delimiter(nodes, "_", TextType.italic_text)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown: str):
    blocks = textwrap.dedent(markdown).strip().split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip() != ""]
    return blocks
