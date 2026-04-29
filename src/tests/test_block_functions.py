import unittest

from block_type import BlockType, block_to_block_type

class TestBlockFunctions(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph block."
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading block."
        self.assertEqual(block_to_block_type(block), BlockType.heading)

    def test_block_to_block_type_code(self):
        block = "```This is a code block.```"
        self.assertEqual(block_to_block_type(block), BlockType.code)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote block."
        self.assertEqual(block_to_block_type(block), BlockType.quote)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is an unordered list block."
        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list block."
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)
