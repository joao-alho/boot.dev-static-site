import unittest

from src.markdown_blocks import (
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_quote,
    block_type_unordered_list,
    markdown_to_blocks,
    markdown_to_html_node,
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
        self.assertEqual(block_to_block_type(heading_block), block_type_heading)
        self.assertEqual(block_to_block_type(quote_block), block_type_quote)
        self.assertEqual(
            block_to_block_type(unordered_block), block_type_unordered_list
        )
        self.assertEqual(block_to_block_type(ordered_block), block_type_ordered_list)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
    - This is a list
    - with items
    - and *more* items

    1. This is an `ordered` list
    2. with items
    3. and more items

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
