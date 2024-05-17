from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode

def main():

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


    print(node.to_html())


main()
