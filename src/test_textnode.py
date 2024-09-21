import unittest

from textnode import TextNode, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "https://www.google.com")
        node2 = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", "bold", "https://www.google.com")
        node2 = TextNode("This is a text node", "light", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", "bold", "https://www.google.com")
        node2 = TextNode("different text", "bold", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.google.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type(self):
        node = text_node_to_html_node(TextNode("This is a text node", "text"))
        self.assertEqual(node.to_html(), "This is a text node")

    def test_bold_type(self):
        node = text_node_to_html_node(TextNode("This is a text node", "bold"))
        self.assertEqual(node.to_html(), "<b>This is a text node</b>")

    def test_italic_type(self):
        node = text_node_to_html_node(TextNode("This is a text node", "italic"))
        self.assertEqual(node.to_html(), "<i>This is a text node</i>")

    def test_code_type(self):
        node = text_node_to_html_node(TextNode("This is a text node", "code"))
        self.assertEqual(node.to_html(), "<code>This is a text node</code>")

    def test_link_type(self):
        node = text_node_to_html_node(
            TextNode("This is a text node", "link", "https://www.google.com")
        )
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">This is a text node</a>'
        )

    def test_image_type(self):
        node = text_node_to_html_node(
            TextNode("This is a image node", "image", "https://imgur.com/anImage.png")
        )
        self.assertEqual(
            node.to_html(),
            '<img src="https://imgur.com/anImage.png" alt="This is a image node"></img>',
        )


if __name__ == "__main__":
    unittest.main()
