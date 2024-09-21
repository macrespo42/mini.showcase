import unittest

from htmlnode import HTMLNode


class TextHTMLNode(unittest.TestCase):
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
