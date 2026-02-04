import unittest
from blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just one block with no extra spacing"
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just one block with no extra spacing"],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """

Paragraph one


Paragraph two



Paragraph three

"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "Paragraph one",
                "Paragraph two",
                "Paragraph three",
            ],
        )

    def test_markdown_to_blocks_only_whitespace(self):
        md = "\n\n   \n\n"
        self.assertEqual(markdown_to_blocks(md), [])

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = """Line one
Line two
Line three"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["Line one\nLine two\nLine three"],
        )
