import unittest

from textnode import TextType, TextNode
from htmlnode import text_node_to_html_node
class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_text(self):
        node = TextNode("This is a bold text node", TextType.bold_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")
    
    def test_italic_text(self):
        node = TextNode("This is an italic text node", TextType.italic_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

    def test_code_text(self):
        node = TextNode("This is a code text node", TextType.code_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
        self.assertEqual(html_node.to_html(), "<code>This is a code text node</code>")

    def test_invalid_text_type(self):
        node = TextNode("This is an invalid text node", "invalid_text_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)