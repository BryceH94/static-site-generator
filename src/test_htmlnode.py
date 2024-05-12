import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Cool Link", children="asdf", props={"href": "google.com", "target": "_blank"})
        results = "href=google.com target=_blank"
        self.assertEqual(node.props_to_html(), results)

    if __name__ == "__main__":
        unittest.main()
