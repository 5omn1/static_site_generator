import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("test_case", "test", [1, 2, 3], {"test1": "value1"})
        node2 = HTMLNode("test_case", "test", [1, 2, 3], {"test1": "value1"})
        self.assertEqual(node1, node2)

    def test_equal_with_value(self):
        node1 = HTMLNode(None, "solo")
        node2 = HTMLNode(None, "solo")
        self.assertEqual(node1, node2)

    def test_equal_with_tag(self):
        node1 = HTMLNode("test_tag")
        node2 = HTMLNode("test_tag")
        self.assertEqual(node1, node2)

    def test_props_to_html_returns_empty_string_when_props_is_none(self):
        node = HTMLNode(props=None)
        assert node.props_to_html() == ""

    def test_props_to_html_returns_empty_string_when_props_is_empty_dict(self):
        node = HTMLNode(props={})
        assert node.props_to_html() == ""

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        assert node.props_to_html() == ' href="https://www.google.com"'

    def test_props_to_html_multiple_props_preserves_insertion_order(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

    def test_props_to_html_values_are_converted_to_string(self):
        node = HTMLNode(props={"data-id": 123, "hidden": True})
        # f-strings call str() on values
        assert node.props_to_html() == ' data-id="123" hidden="True"'
