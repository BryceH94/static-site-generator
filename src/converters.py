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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # For assignment, I can assume proper markdown syntax
    # i.e. no extra whitespace between text and asterisks
    # I can also assume no nested elements like "I am **bold and *italic* text**"

    #TODO FORFUN Add support for nested elements
    #TODO FORFUN Add support for improper markdown
    #TODO BONUS Retain double asterisks when single asterisk is delimiter
    
    result_nodes = list()
    
    for node in old_nodes:
        if node.text_type == "text":
            if delimiter in node.text:
                split_parts = node.text.split(delimiter)

                for i, part in enumerate(split_parts):
                    if i % 2 == 0:
                        result_nodes.append(TextNode(part, "text"))
                    else:
                        if i == len(split_parts) - 1:
                            raise Exception("No closing delimiter found.")
                        else:
                            result_nodes.append(TextNode(part, text_type))
            else:
                result_nodes.append(node) 
        else:
            result_nodes.append(node) 

    return result_nodes