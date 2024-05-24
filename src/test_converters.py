import unittest

from textnode import TextNode
from htmlnode import LeafNode
from converters import text_node_to_html_node
from converters import split_nodes_delimiter

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

    def test_code_node(self):
        node = TextNode("Content", "code")
        expected_result = LeafNode("code", "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_link_node(self):
        node = TextNode("Content", "link", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        expected_result = LeafNode("a", "Content", props={"href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_img_node(self):
        node = TextNode("Content", "image", "https://www.pngfind.com/pngs/m/7-71783_pepe-the-frog-smirk-pepe-hd-png-download.png")
        expected_result = LeafNode("img", "", props=
            {"src": "https://www.pngfind.com/pngs/m/7-71783_pepe-the-frog-smirk-pepe-hd-png-download.png", 
             "alt": "Content"}
            )
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_invalid_text_type(self):
        node = TextNode("Content", "bogus")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    if __name__ == "__main__":
        unittest.main()

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_node(self):
        node = TextNode("This is text with a **bold** word", "text")
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", "bold"), expected_result)

    def test_italic_node(self):
        node = TextNode("This is text with an *italic* word", "text")
        expected_result = [
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected_result)

    def test_code_node(self):
        node = TextNode("This is text with a `code block` word", "text")
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", "code"), expected_result)

    def test_nontext_node_unedited(self):
        node = TextNode("This is all bold and should remain unchanged.", "bold")
        expected_result = [
            TextNode("This is all bold and should remain unchanged.", "bold")
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected_result)

    def test_no_delimiter_returns_unedited(self):
        node = TextNode("I don't have any delimiters!", "text")
        expected_result = [
            TextNode("I don't have any delimiters!", "text")
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected_result)

    def test_no_closing_delimiter(self):
        node = TextNode("I didn't close my *delimiter", "text")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "*", "italic")

    def test_two_italic_node(self):
        node = TextNode("This is text with an *italic* word and *another* one", "text")
        expected_result = [
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and ", "text"),
            TextNode("another", "italic"),
            TextNode(" one", "text")
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", "italic"), expected_result)

    if __name__ == "__main__":
        unittest.main()

