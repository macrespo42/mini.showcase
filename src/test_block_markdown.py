import unittest

from block_markdown import (
    block_to_block_type,
    extract_title,
    markdown_to_block,
    markdown_to_html_node,
)


class TestMarkdownToBlock(unittest.TestCase):
    def test_basics(self):
        text = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        blocks = markdown_to_block(text)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
        * This is a list item
        * This is another list item""",
            ],
        )

    def test_with_lot_of_newlines(self):
        text = """# This is a heading








        This is a paragraph of text. It has some **bold** and *italic* words inside of it.





        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        blocks = markdown_to_block(text)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
        * This is a list item
        * This is another list item""",
            ],
        )

    def test_strip(self):
        text = """# This is a heading                            

                            This is a paragraph of text. It has some **bold** and *italic* words inside of it.     

                             * This is the first list item in a list block
        * This is a list item
        * This is another list item                    """
        blocks = markdown_to_block(text)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
        * This is a list item
        * This is another list item""",
            ],
        )

    def test_with_strip_and_newlines(self):
        text = """# This is a heading                            

















                            This is a paragraph of text. It has some **bold** and *italic* words inside of it.     

















                             * This is the first list item in a list block
        * This is a list item
        * This is another list item                    """
        blocks = markdown_to_block(text)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
        * This is a list item
        * This is another list item""",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_header(self):
        block = "### hello world!"
        self.assertEqual(block_to_block_type(block), "h")

    def test_invalid_header(self):
        block = "###helloworld"
        self.assertEqual(block_to_block_type(block), "p")

        block = "####### helloworld"
        self.assertEqual(block_to_block_type(block), "p")

    def test_code(self):
        block = "```code1\ncode2\ncode3```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_invalid_code(self):
        block = ""
        self.assertEqual(block_to_block_type(block), "p")
        block = "`````"
        self.assertEqual(block_to_block_type(block), "p")

    def test_unordered_list(self):
        block = "* lol\n* tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "ul")
        block = "- lol\n- tbh\n- tbh"
        self.assertEqual(block_to_block_type(block), "ul")
        block = "- lol\n- tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "ul")

    def test_invalid_unordered_list(self):
        block = "*lol\n* tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "-Alol\n- tbh\n- tbh"
        self.assertEqual(block_to_block_type(block), "p")

    def test_ordered_list(self):
        block = "1. lol\n2. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "ol")

    def test_invalid_ordered_list(self):
        block = "1. lol\n4. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "1lol\n4. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "0. lol\n1. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")

    def test_blockquote(self):
        block = "> b1\n> b2\n> b3"
        self.assertEqual(block_to_block_type(block), "blockquote")


class TextMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html(self):
        raw_markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        html_block = markdown_to_html_node(raw_markdown)
        self.assertEqual(
            html_block.to_html(),
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>",
        )

        raw_markdown = """# This is a heading

        * keria\n* faker\n* zeus\n
        
        the cat is in the couch

        ### hello friends !

        hi !!!
        """
        html = markdown_to_html_node(raw_markdown)
        self.assertEqual(
            html.to_html(),
            "<div><h1>This is a heading</h1><ul><li>keria</li><li>faker</li><li>zeus</li></ul><p>the cat is in the couch</p><h3>hello friends !</h3><p>hi !!!</p></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        raw_markdown = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        title = extract_title(raw_markdown)
        self.assertEqual(title, "This is a heading")

        raw_markdown = "# Hello world"
        title = extract_title(raw_markdown)
        self.assertEqual(title, "Hello world")

    def test_fail(self):
        raw_markdown = """## This is secondary heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        with self.assertRaises(ValueError):
            extract_title(raw_markdown)

        raw_markdown = """Hello my friend i don't care about heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block\n* This is a list item\n* This is another list item"""
        with self.assertRaises(ValueError):
            extract_title(raw_markdown)
