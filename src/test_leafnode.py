import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Title")
        self.assertEqual(node.to_html(), "<h1>Title</h1>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "inline text")
        self.assertEqual(node.to_html(), "<span>inline text</span>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode(
            "a", "Google", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Google</a>',
        )

    def test_leaf_to_html_raw_text_when_tag_is_none(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_error_if_value_is_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
