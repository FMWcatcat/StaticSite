from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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
