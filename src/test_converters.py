import unittest

from textnode import (
    TextNode
    ,text_type_text
    ,text_type_bold
    ,text_type_code
    ,text_type_image
    ,text_type_italic
    ,text_type_link
)
from htmlnode import LeafNode, HTMLNode, ParentNode
from converters import (
    text_node_to_html_node
    ,split_nodes_delimiter
    ,split_nodes_image
    ,split_nodes_link
    ,text_to_textnodes
    ,markdown_to_blocks
    ,block_to_block_type
    ,convert_paragraph_block_to_html
    ,convert_code_block_to_html
    ,convert_heading_block_to_html
    ,convert_quote_block_to_html
    ,convert_ulist_block_to_html
    ,block_type_paragraph
    ,block_type_heading
    ,block_type_code
    ,block_type_quote
    ,block_type_unordered_list
    ,block_type_ordered_list
)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node(self):
        node = TextNode("Content", text_type_text)
        expected_result = LeafNode(None, "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_bold_node(self):
        node = TextNode("Content", text_type_bold)
        expected_result = LeafNode("b", "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_italic_node(self):
        node = TextNode("Content", text_type_italic)
        expected_result = LeafNode("i", "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_code_node(self):
        node = TextNode("Content", text_type_code)
        expected_result = LeafNode(text_type_code, "Content")
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_link_node(self):
        node = TextNode("Content", text_type_link, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        expected_result = LeafNode("a", "Content", props={"href": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"})
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_img_node(self):
        node = TextNode("Content", text_type_image, "https://www.pngfind.com/pngs/m/7-71783_pepe-the-frog-smirk-pepe-hd-png-download.png")
        expected_result = LeafNode("img", "", props=
            {"src": "https://www.pngfind.com/pngs/m/7-71783_pepe-the-frog-smirk-pepe-hd-png-download.png", 
             "alt": "Content"}
            )
        self.assertEqual(text_node_to_html_node(node), expected_result)

    def test_invalid_text_type(self):
        node = TextNode("Content", "bogus")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    if __name__ == "__main__":
        unittest.main()

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_node(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode(text_type_bold, text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", text_type_bold), expected_result)

    def test_italic_node(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_italic, text_type_italic),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), expected_result)

    def test_code_node(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        expected_result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", text_type_code), expected_result)

    def test_nontext_node_unedited(self):
        node = TextNode("This is all bold and should remain unchanged.", text_type_bold)
        expected_result = [
            TextNode("This is all bold and should remain unchanged.", text_type_bold)
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), expected_result)

    def test_no_delimiter_returns_unedited(self):
        node = TextNode("I don't have any delimiters!", text_type_text)
        expected_result = [
            TextNode("I don't have any delimiters!", text_type_text)
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), expected_result)

    def test_no_closing_delimiter(self):
        node = TextNode("I didn't close my *delimiter", text_type_text)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "*", text_type_italic)

    def test_two_italic_node(self):
        node = TextNode("This is text with an *italic* word and *another* one", text_type_text)
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_italic, text_type_italic),
            TextNode(" word and ", text_type_text),
            TextNode("another", text_type_italic),
            TextNode(" one", text_type_text)
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", text_type_italic), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestSplitNodesImage(unittest.TestCase):
    def test_one_node_ending_with_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        node = TextNode(text, text_type_text)
        old_nodes = [node]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_result)

    def test_multiple_nodes(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"       
        node = TextNode(text, text_type_text)
        text = " and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) node!"
        node2 = TextNode(text, text_type_text)
        text = "Also text without links!"
        node3 = TextNode(text, text_type_text)
        old_nodes = [node, node2, node3]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
            TextNode(" node!", text_type_text),
            TextNode("Also text without links!", text_type_text)
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_result)

    def test_node_with_link(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [a link](link.link)"
        node = TextNode(text, text_type_text)
        old_nodes = [node]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and [a link](link.link)", text_type_text)
        ]
        self.assertEqual(split_nodes_image(old_nodes), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestSplitNodesLink(unittest.TestCase):
    #I was lazy with these cases since they're basically the same as image
    def test_one_node_ending_with_link(self):
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        node = TextNode(text, text_type_text)
        old_nodes = [node]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_result)

    def test_multiple_nodes(self):
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)"       
        node = TextNode(text, text_type_text)
        text = " and [another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png) node!"
        node2 = TextNode(text, text_type_text)
        text = "Also text without links!"
        node3 = TextNode(text, text_type_text)
        old_nodes = [node, node2, node3]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
            TextNode(" node!", text_type_text),
            TextNode("Also text without links!", text_type_text)
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_result)

    def test_node_with_link(self):
        text = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![a link](link.link)"
        node = TextNode(text, text_type_text)
        old_nodes = [node]
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_image, text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ![a link](link.link)", text_type_text)
        ]
        self.assertEqual(split_nodes_link(old_nodes), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestTextToTextNodes(unittest.TestCase):
    def test_text_with_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", text_type_text),
            TextNode(text_type_text, text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode(text_type_italic, text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(text_type_image, text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode(text_type_link, text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected_result)

    def test_text_with_all_but_one_types(self):
        text = "This is text with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is text with an ", text_type_text),
            TextNode(text_type_italic, text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(text_type_image, text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode(text_type_link, text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(text_to_textnodes(text), expected_result)

    def test_just_text(self):
        text = "This is text"
        expected_result = [
            TextNode("This is text", text_type_text)
        ]

        self.assertEqual(text_to_textnodes(text), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestMarkdownToBlocks(unittest.TestCase):
    def test_text_node(self):
        #How to indent lines in multiline string visual only?
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """

        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ] 
        self.assertEqual(markdown_to_blocks(markdown), expected_result)

    def test_huge_extra_newlines(self):
        markdown = """
        

        
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line






* This is a list
* with items


"""

        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ] 
        self.assertEqual(markdown_to_blocks(markdown), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        text = "## Heading"
        expected_result = block_type_heading
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_not_heading(self):
        text = "##Not Heading"
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_too_many_to_be_heading(self):
        text = "####### Too Long for Heading"
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_code(self):
        text = "```I am some cool code yeah```"
        expected_result = block_type_code
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_not_code_no_closing(self):
        text = "```I am some cool code but I forgot to close myself oops"
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_not_code_not_triple(self):
        text = "`I am some cool code but I forgot to use three`"
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_quote(self):
        line1 = ">I am an elegant quote"
        line2 = ">I still am an elegant quote"
        text = "\n".join([line1, line2])
        expected_result = block_type_quote
        self.assertEqual(block_to_block_type(text), expected_result)
    
    def test_quote_missing_sign(self):
        line1 = ">I am an elegant quote"
        line2 = "I am not an elegant quote"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_unordered_list(self):
        line1 = "* I am a list"
        line2 = "- I still am a list"
        text = "\n".join([line1, line2])
        expected_result = block_type_unordered_list
        self.assertEqual(block_to_block_type(text), expected_result)
    
    def test_ulist_missing_space(self):
        line1 = "* I am a list"
        line2 = "-I am not a list"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_ulist_missing_sign(self):
        line1 = "* I am a list"
        line2 = "I am not a list"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)
    
    def test_olist(self):
        line1 = "1. I am a list"
        line2 = "2. I am also a list"
        text = "\n".join([line1, line2])
        expected_result = block_type_ordered_list
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_long_olist(self):
        lines = [str(i) + ". List Item" for i in range(1,11)]
        text = "\n".join(lines)
        expected_result = block_type_ordered_list
        self.assertEqual(block_to_block_type(text), expected_result)
    
    def test_olist_missing_period(self):
        line1 = "1. I am a list"
        line2 = "2 I am a bad list"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_olist_missing_num(self):
        line1 = "1. I am a list"
        line2 = " I am a bad list"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    def test_olist_wrong_num(self):
        line1 = "1. I am a list"
        line2 = "3. I am a bad list"
        text = "\n".join([line1, line2])
        expected_result = block_type_paragraph
        self.assertEqual(block_to_block_type(text), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestConvertParagraphBlockToHTML(unittest.TestCase):
    def test_text_with_bold(self):
        text = "I am text with a **bold** word."
        expected_result = ParentNode("p", children=[
            LeafNode(None, "I am text with a "),
            LeafNode("b", text_type_bold),
            LeafNode(None, " word.")
        ])
        self.assertEqual(convert_paragraph_block_to_html(text), expected_result)
    
    def test_text_with_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)."
        expected_result = ParentNode("p", children=[
            LeafNode(None, "This is text with an "),
            LeafNode("img", "", props={"src": "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png", "alt": text_type_image}),
            LeafNode(None, ".")
        ])
        self.assertEqual(convert_paragraph_block_to_html(text), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestConvertCodeBlockToHTML(unittest.TestCase):
    def test_one_line_of_code(self):
        text = "```I am some nice code.```"
        expected_result = ParentNode("pre", children=[
            LeafNode("code", "I am some nice code.")
        ])
        self.assertEqual(convert_code_block_to_html(text), expected_result)

    def test_multiple_lines_of_code(self):
        text = """```I am some nice code.
I have a second line.        
```"""
        expected_result = ParentNode("pre", children=[
            LeafNode("code", "I am some nice code.\nI have a second line.")
        ])
        self.assertEqual(convert_code_block_to_html(text), expected_result)
 
    if __name__ == "__main__":
        unittest.main()

class TestConvertHeadingBlockToHTML(unittest.TestCase):
    def test_h2_heading(self):
        text = "## I am a heading"
        expected_result = LeafNode("h2", "I am a heading") 
        self.assertEqual(convert_heading_block_to_html(text), expected_result)
    
    def test_h2_heading_with_whitespace(self):
        text = "##   I am a heading with extra whitespace  "
        expected_result = LeafNode("h2", "I am a heading with extra whitespace") 
        self.assertEqual(convert_heading_block_to_html(text), expected_result)
 
    if __name__ == "__main__":
        unittest.main()

class TestConvertQuoteBlockToHTML(unittest.TestCase):
    def test_single_line_quote(self):
        text = "> I am a small quote"
        expected_result = LeafNode("blockquote", "I am a small quote") 
        self.assertEqual(convert_quote_block_to_html(text), expected_result)
    
    def test_multi_line_quote(self):
        text = """> I am a small quote
> But I have a second line"""
        expected_result = LeafNode("blockquote", "I am a small quote\nBut I have a second line")
        self.assertEqual(convert_quote_block_to_html(text), expected_result)
 
    if __name__ == "__main__":
        unittest.main()

class TestConvertUlistBlockToHTML(unittest.TestCase):
    def test_single_line_list(self):
        text = "* I am a brief list with **bolded** text"
        expected_result = ParentNode("ul", children=[
            ParentNode("li", children=[
                LeafNode(None, "I am a brief list with "),
                LeafNode(text_type_bold, "bolded"),
                LeafNode(None, " text")
            ])
        ])
        self.assertEqual(convert_ulist_block_to_html(text), expected_result)
    
    def test_multi_line_list(self):
        text = """* I am a list with **bolded** text
- I am a list item with *italic* text
* I am a list item with a ![cool image](coolurl.com)"""
        expected_result = ParentNode("ul", children=[
            ParentNode("li", children=[
                LeafNode(None, "I am a list with "),
                LeafNode(text_type_bold, "bolded"),
                LeafNode(None, " text")
            ]),
            ParentNode("li", children=[
                LeafNode(None, "I am a list item with "),
                LeafNode(text_type_italic, "italic"),
                LeafNode(None, " text")
            ]),
            ParentNode("li", children=[
                LeafNode(None, "I am a list item with a "),
                LeafNode("img", "", props={"src": "coolrul.com", "alt": "cool image"})
            ])
        ])
        self.assertEqual(convert_ulist_block_to_html(text), expected_result)
 
    if __name__ == "__main__":
        unittest.main()

