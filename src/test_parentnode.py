import unittest

from htmlnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_tag_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(children="asdf", props={"href": "google.com", "target": "_blank"})

    def test_children_required(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="a", props={"href": "google.com", "target": "_blank"})

    #TODO Test Cases
    # Test only leafNodes
    # Test only parentNodes, flat
    # Test nested only parentNodes
    # Test leafNodes and parentNodes with both parents and leafNodes within
    # Single Parent node
    # Single leaf node child

    if __name__ == "__main__":
        unittest.main()
