import unittest
from src.markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_code,
    block_type_paragraph,
    block_type_quote,
    block_type_heading,
    block_type_unordered_list,
    block_type_ordered_list
)


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items"""

        self.assertEqual(len(markdown_to_blocks(markdown)), 3)

    def test_block_to_block_type(self):
        code_block = """```\nprint("hello")\n```"""
        heading_block = "## HEADING"
        quote_block = ">this will be\n>a quote"
        unordered_block = "* this\n* is a\n- list"
        ordered_block = "1. this\n2. is a\n3. list"

        self.assertEqual(block_to_block_type(code_block), block_type_code)
        self.assertEqual(block_to_block_type(
            heading_block), block_type_heading)
        self.assertEqual(block_to_block_type(quote_block), block_type_quote)
        self.assertEqual(block_to_block_type(
            unordered_block), block_type_unordered_list)
        self.assertEqual(block_to_block_type(
            ordered_block), block_type_ordered_list)
