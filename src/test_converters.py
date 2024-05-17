import unittest

from textnode import TextNode
from htmlnode import LeafNode
from converters import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node(self):
        node = TextNode("Content", "text")
        expected_result = LeafNode(None, "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_bold_node(self):
        node = TextNode("Content", "bold")
        expected_result = LeafNode("b", "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_italic_node(self):
        node = TextNode("Content", "italic")
        expected_result = LeafNode("i", "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)


    #TODO test casee
    # code node
    # link node
    # img node
    # other node (should error)

    if __name__ == "__main__":
        unittest.main()
