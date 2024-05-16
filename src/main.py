from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode

def main():

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            ParentNode(tag="p", children=[
                LeafNode(None, "I'm in a parent")
            ]),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())


main()
