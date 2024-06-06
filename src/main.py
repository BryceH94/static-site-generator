from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from generators import generate_pages_recursive

def main():
    generate_pages_recursive("content", "template.html", "public")


main()
