import unittest

from src.htmlnode import HTMLNode
from src.htmlnode import LeafNode
from src.htmlnode import ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_children_nodes(self):
        node = HTMLNode(
            "tag", "value", props={"href": "https://www.google.com", "target": "_blank"}
        )
        node_1 = HTMLNode(children=[node])

        self.assertEqual(node_1.children[0], node)

    def test_props_to_html(self):
        node = HTMLNode(
            "tag", "value", props={"href": "https://www.google.com", "target": "_blank"}
        )

        html_props = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), html_props)

    def test_leaf_node(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node1_should_render_as = "<p>This is a paragraph of text.</p>"
        node2_should_render_as = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node1.to_html(), node1_should_render_as)
        self.assertEqual(node2.to_html(), node2_should_render_as)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.to_html(), "hello")

    def test_parent_node(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node1_should_render_as = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node1.to_html(), node1_should_render_as)

    def test_nested_parent_node(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode("p", [LeafNode(None, "hello")]),
            ],
        )
        node1_should_render_as = (
            "<p><b>Bold text</b>Normal text<i>italic text</i><p>hello</p></p>"
        )
        self.assertEqual(node1.to_html(), node1_should_render_as)


if __name__ == "__main__":
    unittest.main()
