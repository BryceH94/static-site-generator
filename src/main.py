from textnode import TextNode
from htmlnode import LeafNode

def main():
    testNode = LeafNode(tag="a", value="Cool Link", props={"href": "google.com", "target": "_blank"})
    print(testNode.to_html())

main()
