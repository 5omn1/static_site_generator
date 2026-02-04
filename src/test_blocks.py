import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType


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

    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        self.assertEqual(block_to_block_type("#Hello"), BlockType.PARAGRAPH)

    def test_heading_invalid_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Hello"), BlockType.PARAGRAPH)

    def test_code_block_multiline(self):
        md = "```\nline1\nline2\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_code_block_invalid_missing_newline_after_ticks(self):
        md = "```code\n```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        md = "> q1\n>q2\n> q3"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_quote_invalid_mixed_lines(self):
        md = "> q1\nnot quote"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        md = "- a\n- b\n- c"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_missing_space(self):
        md = "- a\n-b"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_valid(self):
        md = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_not_starting_at_one(self):
        md = "2. a\n3. b"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_not_incrementing(self):
        md = "1. a\n3. b"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_missing_space(self):
        md = "1. a\n2.b"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_paragraph_default(self):
        md = "This is a normal paragraph.\nStill same block."
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
