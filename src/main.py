from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode
from file_utils import copy_directory
from generators import generate_page

def main():
    #copy_directory()
    generate_page("content/index.md", "template.html", "public/index.html")


main()
