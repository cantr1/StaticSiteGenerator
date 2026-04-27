import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        properties = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        node = HTMLNode(props = properties)

        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())
    
    def test_repr(self):
        properties = {
            "href": "https://www.google.com",
            "target": "java",
        }
        tag = "plain text"
        value = "Should I learn Java?"

        node = HTMLNode(tag=tag, value=value, props=properties)

        self.assertEqual(repr(node),
        f"HTMLNode - tag: {node.tag}, value: {node.value}, children: {node.children}, props: {node.props}")

    def test_repr_no_props(self):
        tag = "plain text"
        value = "Should I learn Java?"

        node = HTMLNode(tag=tag, value=value)

        self.assertEqual(repr(node),
        f"HTMLNode - tag: {node.tag}, value: {node.value}, children: {node.children}, props: {node.props}")

    def test_values(self):
        tag = "plain text"
        value = "Should I learn Java?"
        children = [HTMLNode(tag="child", value="child node")]

        node = HTMLNode(tag=tag, value=value, children=children)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {})