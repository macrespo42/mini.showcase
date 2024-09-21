import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        html = HTMLNode()
        self.assertRaises(NotImplementedError, html.to_html)

    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        html = HTMLNode(props=props)
        self.assertEqual(
            html.props_to_html(), 'href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
        html = HTMLNode(tag="p", value="hello world")
        self.assertEqual(html.__repr__(), "HTMLNode(p, hello world, None, None)")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf = LeafNode("p", "This is a paragraph of text.")
        leaf1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(leaf.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(
            leaf1.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_errors(self):
        leaf = LeafNode("p", None)
        self.assertRaises(ValueError, leaf.to_html)

    def test_html_without_tags(self):
        leaf = LeafNode(None, "This is a paragraph of text.")
        self.assertEqual(leaf.to_html(), "This is a paragraph of text.")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(
            ValueError,
            node.to_html,
        )

    def test_to_html_no_children(self):
        node = ParentNode(
            "p",
            [],
        )
        self.assertRaises(
            ValueError,
            node.to_html,
        )

    def test_to_html_none_childs(self):
        node = ParentNode(
            "p",
            None,
        )
        self.assertRaises(
            ValueError,
            node.to_html,
        )
