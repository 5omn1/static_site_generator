import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_h1_inline(self):
        md = "# Hello **world**"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Hello <b>world</b></h1></div>")

    def test_heading_h3(self):
        md = "### Title"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h3>Title</h3></div>")

    def test_quote_multiline(self):
        md = """
> This is a quote with **bold**
> and a second line with _italics_
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with <b>bold</b> and a second line with <i>italics</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- first **item**
- second item
- third _item_
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first <b>item</b></li><li>second item</li><li>third <i>item</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. one
2. two **bold**
3. three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two <b>bold</b></li><li>three</li></ol></div>",
        )


def test_mixed_blocks(self):
    md = """
# Heading

Paragraph with a [link](https://boot.dev) and an ![img](u).

- item 1
- item 2

> quoted `code`
"""
    node = markdown_to_html_node(md)
    self.assertEqual(
        node.to_html(),
        "<div>"
        "<h1>Heading</h1>"
        '<p>Paragraph with a <a href="https://boot.dev">link</a> and an <img src="u" alt="img"></img>.</p>'
        "<ul><li>item 1</li><li>item 2</li></ul>"
        "<blockquote>quoted <code>code</code></blockquote>"
        "</div>",
    )


def test_empty_markdown(self):
    md = "   \n\n   "
    node = markdown_to_html_node(md)
    self.assertEqual(node.to_html(), "<div></div>")
