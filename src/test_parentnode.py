import unittest

from htmlnode import ParentNode


class TestParentNode(unittest.TestCase):
    # no value argument, tag required, children required
    def test_tag_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(children="asdf", props={"href": "google.com", "target": "_blank"})

    def test_children_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="a", props={"href": "google.com", "target": "_blank"})

    if __name__ == "__main__":
        unittest.main()
