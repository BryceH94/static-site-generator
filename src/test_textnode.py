import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_with_urls(self):
        node = TextNode("This is a text node", "bold", "cool.com")
        node2 = TextNode("This is a text node", "bold", "cool.com")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a slighlty different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_one_none(self):
        node = TextNode("This is a text node", "bold", "bogus.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_not_eq_urls(self):
        node = TextNode("This is a text node", "bold", "bogus.com")
        node2 = TextNode("This is a text node", "bold", "bologna.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
