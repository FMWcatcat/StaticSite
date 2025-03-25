import unittest
from htmlnode import HTMLNODE

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

if __name__ == "__main__":
    unittest.main()