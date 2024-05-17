from htmlnode import HTMLNode, LeafNode
from textnode import TextNode

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})

    raise ValueError("invalid text type provided")