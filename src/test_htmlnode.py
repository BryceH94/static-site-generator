import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="a", value="Cool Link", children="asdf", props={"href": "google.com", "target": "_blank"})
        expected_result = 'href="google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_result)

    if __name__ == "__main__":
        unittest.main()
