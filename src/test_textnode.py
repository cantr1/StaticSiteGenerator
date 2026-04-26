import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a test node", TextType.bold_text)
        node2 = TextNode("This is a test node", TextType.bold_text)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a test node", TextType.bold_text)
        node2 = TextNode("This is a dev node", TextType.bold_text)
        self.assertNotEqual(node1, node2)

    def test_type_mismatch(self):
        node1 = TextNode("This is a test node", TextType.bold_text)
        node2 = TextNode("This is a test node", TextType.italic_text)
        self.assertNotEqual(node1, node2)

    def test_url_mismatch(self):
        node1 = TextNode("This is a test node", TextType.bold_text, "www.google.com")
        node2 = TextNode("This is a test node", TextType.bold_text, "www.bing.com")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a test node", TextType.bold_text, "www.google.com")
        expected_repr = "TextNode(This is a test node, **Bold text**, www.google.com)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()