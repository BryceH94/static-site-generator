import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    # def test_eq(self):
    #     node = HTMLNode("<a>", "Cool Link", "asdf", {"href": "google.com", "target": "_blank"})
    #     node2 = HTMLNode("<a>", "Cool Link", "asdf", {"href": "google.com", "target": "_blank"})
    #     self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("<a>", "Cool Link", "asdf", {"href": "google.com", "target": "_blank"})
        results = "href=google.com target=_blank"
        self.assertEqual(node.props_to_html(), results)

    if __name__ == "__main__":
        unittest.main()
