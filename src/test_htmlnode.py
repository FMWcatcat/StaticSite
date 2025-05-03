import unittest
from htmlnode import HTMLNODE
from htmlnode import LeafNode

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





if __name__ == "__main__":
    unittest.main()


