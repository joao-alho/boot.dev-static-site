import unittest

from src.htmlnode import LeafNode
from src.textnode import TextNode, text_node_to_html_node
from src.inline_markdown import split_nodes_delimiter, text_type_text, text_type_code


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text mode", "bold")
        node2 = TextNode("This is a text mode", "bold")
        self.assertEqual(node, node2)

    def test_node_to_html_node(self):
        node = TextNode("This is a text node", "bold")
        result = LeafNode(tag="b", value="This is a text node")
        self.assertEqual(text_node_to_html_node(node), result)

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_raises_error(self):
        node = TextNode("This is text with a code block` word", text_type_text)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", text_type_code)

    def test_split_nodes_dont_split(self):
        node = TextNode("This is text with a `code block` word", text_type_code)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(new_nodes, [node])


if __name__ == "__main__":
    unittest.main()
