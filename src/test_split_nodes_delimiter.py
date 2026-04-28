import unittest

from textnode import TextType, TextNode
from htmlnode import text_node_to_html_node
from helper_functions import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code_text)

        self.assertEqual([
        TextNode("This is text with a ", TextType.text),
        TextNode("code block", TextType.code_text),
        TextNode(" word", TextType.text),
        ], new_nodes)
    
    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is text without a code block word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code_text)

        self.assertEqual([
        TextNode("This is text without a code block word", TextType.text),
        ], new_nodes)
    
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded", TextType.bold_text),
                TextNode(" word and ", TextType.text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("bolded word", TextType.bold_text),
                TextNode(" and ", TextType.text),
                TextNode("another", TextType.bold_text),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text),
                TextNode("italic", TextType.italic_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold_text)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.italic_text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.bold_text),
                TextNode(" and ", TextType.text),
                TextNode("italic", TextType.italic_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code_text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text),
                TextNode("code block", TextType.code_text),
                TextNode(" word", TextType.text),
            ],
            new_nodes,
        )
