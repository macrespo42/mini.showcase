import unittest

from block_markdown import markdown_to_block


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
