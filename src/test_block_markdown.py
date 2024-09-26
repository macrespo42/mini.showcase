import unittest

from block_markdown import block_to_block_type, markdown_to_block


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
        self.assertEqual(block_to_block_type(block), "header")

    def test_invalid_header(self):
        block = "###helloworld"
        self.assertEqual(block_to_block_type(block), "p")

        block = "####### helloworld"
        self.assertEqual(block_to_block_type(block), "p")

    def test_code(self):
        block = "```> code1\n> code2\n> code3```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_invalid_code(self):
        block = "```> code1\ncode2\n> code3```"
        self.assertEqual(block_to_block_type(block), "p")
        block = ""
        self.assertEqual(block_to_block_type(block), "p")
        block = "`````"
        self.assertEqual(block_to_block_type(block), "p")

    def test_unordered_list(self):
        block = "* lol\n* tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "- lol\n- tbh\n- tbh"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "- lol\n- tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_invalid_unordered_list(self):
        block = "*lol\n* tbh\n* tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "-Alol\n- tbh\n- tbh"
        self.assertEqual(block_to_block_type(block), "p")

    def test_ordered_list(self):
        block = "1. lol\n2. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_invalid_ordered_list(self):
        block = "1. lol\n4. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "1lol\n4. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")
        block = "0. lol\n1. tbh\n3. tbh"
        self.assertEqual(block_to_block_type(block), "p")
