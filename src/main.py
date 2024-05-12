from textnode import TextNode
from htmlnode import HTMLNode

def main():
    testNode = HTMLNode("<a>", "Cool Link", "asdf", {"href": "google.com", "target": "_blank"})
    print(testNode.props_to_html())

main()
