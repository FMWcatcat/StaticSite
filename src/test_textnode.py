import unittest
import sys
import os
from textnode import TextNode, TextType
from textnode import markdown_to_blocks, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_simple(self):
        text = "Hello, world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Hello, world!")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertIsNone(nodes[0].url)
    
    def test_text_to_textnodes_bold(self):
        text = "Hello, **bold** world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello, ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " world!")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_italic(self):
        text = "Hello, _italic_ world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello, ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " world!")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_code(self):
        text = "Hello, `code` world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello, ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " world!")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_image(self):
        text = "Hello, ![alt text](https://example.com/image.png) world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello, ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "alt text")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/image.png")
        self.assertEqual(nodes[2].text, " world!")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_link(self):
        text = "Hello, [link text](https://example.com) world!"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello, ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link text")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
        self.assertEqual(nodes[2].text, " world!")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_text_to_textnodes_combined(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/image.png) and a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[7].text, "image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://example.com/image.png")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://example.com")



class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks(self):

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_single_block(self):

        md = "Just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one block"])
    
    def test_extra_newlines(self):
        # Test with excessive newlines
        md = """
Block 1


Block 2



Block 3
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

if __name__ == "__main__":
    unittest.main()

