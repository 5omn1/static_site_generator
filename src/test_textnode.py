import unittest

from textnode import TextNode, TextType


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
        node1 = TextNode("hello", TextType.PLAIN)
        node2 = TextNode("world", TextType.PLAIN)
        self.assertNotEqual(node1, node2)

    def test_different_text_type_not_equal(self):
        node1 = TextNode("hello", TextType.PLAIN)
        node2 = TextNode("hello", TextType.BOLD)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
