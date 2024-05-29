from htmlnode import HTMLNode, LeafNode
from textnode import TextNode
from extractors import extract_markdown_images
from extractors import extract_markdown_links

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list =  "ordered_list"

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

def split_nodes_image(old_nodes):
    result_nodes = list ()

    for node in old_nodes:
        if node.text_type == "text":
            images = extract_markdown_images(node.text)
            if images:
                text_after = node.text
                for img in images:
                    text_before, text_after = text_after.split(f"![{img[0]}]({img[1]})", 1)
                    result_nodes.append(TextNode(text_before,"text"))
                    result_nodes.append(TextNode(img[0], "image", img[1])) 
                if text_after:
                    result_nodes.append(TextNode(text_after,"text"))
            else:
                result_nodes.append(node) 
        else:
            result_nodes.append(node) 

    return result_nodes

def split_nodes_link(old_nodes):
    result_nodes = list ()

    for node in old_nodes:
        if node.text_type == "text":
            links = extract_markdown_links(node.text)
            if links:
                text_after = node.text
                for link in links:
                    text_before, text_after = text_after.split(f"[{link[0]}]({link[1]})", 1)
                    result_nodes.append(TextNode(text_before,"text"))
                    result_nodes.append(TextNode(link[0], "link", link[1])) 
                if text_after:
                    result_nodes.append(TextNode(text_after,"text"))
            else:
                result_nodes.append(node) 
        else:
            result_nodes.append(node) 

    return result_nodes

def text_to_textnodes(text):
    starter_node = TextNode(text, "text")
    new_nodes = split_nodes_delimiter([starter_node], "**", "bold")
    new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
    new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    return list(filter(lambda text: len(text) > 0, map(lambda block: block.strip(),  markdown.split("\n\n"))))

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    headings = tuple(['#' * i + ' ' for i in range(1,7)])

    if markdown_block.startswith(headings):
        if len(lines) == 1:
            #Can a heading have text directly beneath (i.e. only one newline)?
            return block_type_heading
    if markdown_block.startswith('```') and markdown_block.endswith('```'):
        return block_type_code
    if markdown_block.startswith('>'):
        if len(filter(lambda line: line.startswith('>'))) == len(lines):
            return block_type_quote
    if markdown_block.startswith(('* ', '- ')):
        if len(filter(lambda line: line.startswith(('* ', '- ')))) == len(lines):
            return block_type_unordered_list
    if markdown_block[0].isdigit():
        for i, line in enumerate(lines):
            num, text = line.split('. ', maxsplit=1)
            if num.isdigit() and int(num) == i + 1 and text is not None:
                continue
            else:
                return block_type_paragraph
        return block_type_ordered_list

    return block_type_paragraph