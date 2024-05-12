import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_children_not_allowed(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", value="Cool Link", children="asdf", props={"href": "google.com", "target": "_blank"})

    def test_value_required(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="a", value=None, children=None, props={"href": "google.com", "target": "_blank"})

    def test_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Cool Info", children=None, props=None)
        expected_result = 'Cool Info'
        self.assertEqual(node.to_html(),expected_result)

    def test_to_html_tag_no_props(self):
        node = LeafNode(tag="p", value="Cool Info", children=None, props=None)
        expected_result = '<p>Cool Info</p>'
        self.assertEqual(node.to_html(),expected_result)

    def test_to_html_tag_with_props(self):
        node = LeafNode(tag="a", value="Cool Link", children=None, props={"href": "google.com", "target": "_blank"})
        expected_result = '<a href="google.com" target="_blank">Cool Link</a>'
        self.assertEqual(node.to_html(),expected_result)

    if __name__ == "__main__":
        unittest.main()
