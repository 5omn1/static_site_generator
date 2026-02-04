import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_raises_if_tag_is_none(self):
        parent_node = ParentNode(None, [LeafNode("span", "x")])
        with self.assertRaises(ValueError) as ctx:
            parent_node.to_html()
        self.assertIn("tag", str(ctx.exception).lower())

    def test_parent_raises_if_children_is_none(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as ctx:
            parent_node.to_html()
        self.assertIn("children", str(ctx.exception).lower())

    def test_to_html_with_no_children_empty_list(self):
        # children missing (None) should raise, but an empty list is allowed by spec
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "one")
        child2 = LeafNode("b", "two")
        child3 = LeafNode("i", "three")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>one</span><b>two</b><i>three</i></div>",
        )

    def test_to_html_mixed_leaf_text_and_tag_children(self):
        # LeafNode with tag=None returns raw text
        child1 = LeafNode(None, "Hello ")
        child2 = LeafNode("b", "world")
        parent_node = ParentNode("p", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<p>Hello <b>world</b></p>")

    def test_to_html_parent_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], props={"class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container" id="main"><span>child</span></div>',
        )

    def test_to_html_nested_parents_multiple_levels(self):
        # div -> section -> p -> (text + strong)
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [LeafNode(None, "Hi "), LeafNode("strong", "there")],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><p>Hi <strong>there</strong></p></section></div>",
        )

    def test_to_html_two_sibling_parent_nodes(self):
        # div -> (span -> b) + (span -> i)
        left = ParentNode("span", [LeafNode("b", "L")])
        right = ParentNode("span", [LeafNode("i", "R")])
        node = ParentNode("div", [left, right])
        self.assertEqual(
            node.to_html(), "<div><span><b>L</b></span><span><i>R</i></span></div>"
        )
