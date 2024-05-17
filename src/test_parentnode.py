import unittest

from htmlnode import ParentNode
from htmlnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_tag_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(children="asdf", props={"href": "google.com", "target": "_blank"})

    def test_children_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="a", props={"href": "google.com", "target": "_blank"})

    def test_leaf_nodes(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
        expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(),expected_result)

    def test_parent_nodes(self):
        node = ParentNode(
                "p",
                [
                    ParentNode(tag="p", children=[
                        LeafNode(None, "I'm in a parent")
                    ]),
                    ParentNode(tag="b", children=[
                        LeafNode(None, "I'm boldly in a parent")
                    ]),
                ],
            )
        expected_result = "<p><p>I'm in a parent</p><b>I'm boldly in a parent</b></p>"
        self.assertEqual(node.to_html(),expected_result)

    def test_nested_nodes(self):
        node = ParentNode(
                "p",
                [
                    ParentNode(tag="p", children=[
                        LeafNode(None, "I'm in a parent"),
                        ParentNode(tag="b", children=[
                            LeafNode(None, "I'm boldly nested in a parent"),
                            ParentNode(tag="a", children=[
                                LeafNode(None, "I got links baby"),
                            ], props={"href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}),
                            LeafNode("p", "I'm nested with my sibling")
                        ]),
                    ]),
                ],
            )

        expected_result = "<p><p>I'm in a parent<b>I'm boldly nested in a parent<a href=\"https://www.youtube.com/watch?v=dQw4w9WgXcQ\">I got links baby</a><p>I'm nested with my sibling</p></b></p></p>"
        self.assertEqual(node.to_html(),expected_result)

    def test_single_parent_node(self):
        node = ParentNode("p", children=[LeafNode(None, "Content")])
        expected_result = "<p>Content</p>"
        self.assertEqual(node.to_html(), expected_result)

    def test_single_leaf_node(self):
        node = LeafNode(None, "Content")
        expected_result = "Content"
        self.assertEqual(node.to_html(), expected_result)

    if __name__ == "__main__":
        unittest.main()
