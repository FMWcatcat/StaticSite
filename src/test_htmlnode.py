import unittest
from htmlnode import HTMLNODE
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_links, extract_markdown_images 

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNODE(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    def test_props_to_html_with_single_prop(self):
        node = HTMLNODE(props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')
        
    def test_props_to_html_with_no_props(self):
        node = HTMLNODE()
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")




class TestLeafNode(unittest.TestCase):
    def test_with_tag(self):
        node = LeafNode("p", "A paragraph!")
        self.assertEqual(node.to_html(), "<p>A paragraph!</p>")

    def test_with_tag(self):
        node = LeafNode(None, "Just text.")
        self.assertEqual(node.to_html(), "Just text.")


def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )



if __name__ == "__main__":
    unittest.main()




class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        # Test when the delimiter isn't in the text
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_simple_delimiter(self):
        # Test with a single delimiter pair
        node = TextNode("Text with **bold** content", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Text with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " content")
        self.assertEqual(result[2].text_type, TextType.TEXT)
    
    def test_delimiter_at_start(self):
        # Test with delimiter at the start
        node = TextNode("**Bold** at the beginning", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Bold")
        self.assertEqual(result[0].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, " at the beginning")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    
class TestMarkdownExtraction(unittest.TestCase):
    
    def test_extract_markdown_images_single(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        text = "Multiple images: ![first](https://example.com/first.jpg) and ![second](https://example.com/second.png)"
        matches = extract_markdown_images(text)
        expected = [
            ("first", "https://example.com/first.jpg"),
            ("second", "https://example.com/second.png")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_images_none(self):
        text = "This text has no images, only [a link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_multiple(self):
        text = "Multiple links: [first](https://example.com) and [second](https://another.com)"
        matches = extract_markdown_links(text)
        expected = [
            ("first", "https://example.com"),
            ("second", "https://another.com")
        ]
        self.assertListEqual(expected, matches)
    
    def test_extract_markdown_links_none(self):
        text = "This text has no links, only an ![image](https://example.com/img.jpg)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_and_images(self):
        text = "This has a [link](https://example.com) and an ![image](https://example.com/img.jpg)"
        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("link", "https://example.com")], link_matches)
        self.assertListEqual([("image", "https://example.com/img.jpg")], image_matches)
    
    def test_extract_markdown_links_with_special_chars(self):
        text = "Link with [special chars in title!](https://example.com/path?query=value#fragment)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("special chars in title!", "https://example.com/path?query=value#fragment")], matches)
    
    def test_extract_markdown_empty_string(self):
        matches_links = extract_markdown_links("")
        matches_images = extract_markdown_images("")
        self.assertListEqual([], matches_links)
        self.assertListEqual([], matches_images)