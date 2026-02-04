import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_with_url(self):
        node1 = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        node2 = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        self.assertEqual(node1, node2)

    def test_different_url_not_equal(self):
        node1 = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        node2 = TextNode("OpenAI", TextType.LINK, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_different_text_not_equal(self):
        node1 = TextNode("hello", TextType.TEXT)
        node2 = TextNode("world", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_different_text_type_not_equal(self):
        node1 = TextNode("hello", TextType.TEXT)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold!")

    def test_italic(self):
        node = TextNode("Italic!", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic!")

    def test_code(self):
        node = TextNode("print('hi')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")

    def test_link(self):
        node = TextNode("OpenAI", TextType.LINK, "https://openai.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "OpenAI")
        self.assertEqual(html_node.props, {"href": "https://openai.com"})

    def test_image(self):
        node = TextNode("cute cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/cat.png", "alt": "cute cat"}
        )

    def test_link_missing_url_raises(self):
        node = TextNode("Broken link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_missing_url_raises(self):
        node = TextNode("Broken image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_splits_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_leaves_non_text_nodes_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_multiple_code_blocks_in_one_node(self):
        node = TextNode("a `b` c `d` e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_does_not_create_empty_nodes_when_delimiters_touch_text_edges(self):
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_raises_on_unmatched_delimiter(self):
        node = TextNode("This is `broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_splits_only_text_nodes_in_mixed_list(self):
        nodes = [
            TextNode("start `mid` end", TextType.TEXT),
            TextNode("keep me", TextType.ITALIC),
            TextNode("x `y` z", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("start ", TextType.TEXT),
            TextNode("mid", TextType.CODE),
            TextNode(" end", TextType.TEXT),
            TextNode("keep me", TextType.ITALIC),
            TextNode("x ", TextType.TEXT),
            TextNode("y", TextType.CODE),
            TextNode(" z", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images_multiple(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_none(self):
        text = "No images here, just text and a [link](https://example.com)."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_images_allows_empty_alt(self):
        text = "Empty alt: ![](https://example.com/x.png)"
        expected = [("", "https://example.com/x.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_does_not_match_normal_links(self):
        text = "A normal link: [OpenAI](https://openai.com)"
        self.assertEqual(extract_markdown_images(text), [])

    # ---- extract_markdown_links ----

    def test_extract_markdown_links_multiple(self):
        text = (
            "This has [OpenAI](https://openai.com) and "
            "[Example](https://example.com/page)."
        )
        expected = [
            ("OpenAI", "https://openai.com"),
            ("Example", "https://example.com/page"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_none(self):
        text = "No links here, just ![img](https://example.com/a.png)."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_links_does_not_match_images(self):
        text = "An image: ![alt](https://example.com/a.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_links_mixed_links_and_images(self):
        text = (
            "Mix: ![pic](https://img.com/a.png) and "
            "[site](https://example.com) and "
            "![pic2](https://img.com/b.png) and "
            "[docs](https://example.com/docs)"
        )
        expected = [
            ("site", "https://example.com"),
            ("docs", "https://example.com/docs"),
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_allows_empty_anchor_and_url(self):
        text = "Empty: []()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected)


if __name__ == "__main__":
    unittest.main()
