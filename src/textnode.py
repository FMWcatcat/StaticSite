import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
)
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            text = old_node.text
            start_index = text.find(delimiter)
            if start_index == -1:
                new_nodes.append(old_node)
            else:
                end_index = text.find(delimiter, start_index + len(delimiter))
                if end_index == -1:
                    raise Exception("Invalid markdown syntax: missing closing delimiter")
                else:
                    before_text = text[:start_index]
                    delimiter_text = text[start_index + len(delimiter):end_index]
                    after_text = text[end_index + len(delimiter):]
                    if before_text:
                        new_nodes.append(TextNode(before_text, TextType.TEXT))
                    if delimiter_text:
                        new_nodes.append(TextNode(delimiter_text, text_type))
                    if after_text:
                        new_nodes.append(TextNode(after_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern,text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern,text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        images = extract_markdown_images(text)
        while images:
            alt, url = images[0]
            before, after = text.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
            images = extract_markdown_images(text)
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))           
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        links = extract_markdown_links(text)
        while links:
            alt, url = links[0]
            before, after = text.split(f"[{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = after
            links = extract_markdown_links(text)
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))           
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    old_nodes_count = -1
    while old_nodes_count != len(nodes):
        old_nodes_count = len(nodes)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    old_nodes_count = -1
    while old_nodes_count != len(nodes):
        old_nodes_count = len(nodes)   
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  
    old_nodes_count = -1
    while old_nodes_count != len(nodes):
        old_nodes_count = len(nodes)     
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            processed_blocks.append(stripped_block)
    return processed_blocks

def block_to_block_type(block):
    lines = block.splitlines()

    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.code
    elif re.match("^#{1,6} ", block):
        return BlockType.heading
    elif block.startswith(">"):
        return BlockType.quote
    elif for line in lines:
            if not line.startswith(f"- "):    
                break
        else:
            return BlockType.unordered_list
    else:
        expected_number = 1
        for line in lines:
            if line.startswith(f"{expected_number}. "):
                expected_number += 1
            else:
                break
        else:
            return BlockType.ordered_list
    
    return BlockType.paragraph




