from enum import Enum, auto
from leafnode import LeafNode


class TextType(Enum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    text = text_node.text
    text_node_text_type = text_node.text_type
    url = getattr(text_node, "url", None)

    if text_node_text_type == TextType.TEXT:
        return LeafNode(None, text)
    if text_node_text_type == TextType.BOLD:
        return LeafNode("b", text)
    if text_node_text_type == TextType.ITALIC:
        return LeafNode("i", text)
    if text_node_text_type == TextType.CODE:
        return LeafNode("code", text)
    if text_node_text_type == TextType.LINK:
        if not url:
            raise ValueError("LINK TextNode requires a url")
        return LeafNode("a", text, {"href": url})
    if text_node_text_type == TextType.IMAGE:
        if not url:
            raise ValueError("IMAGE TextNode requires a url")
        return LeafNode("img", "", {"src": url, "alt": text})
    raise ValueError(f"Unknown TextType {text_node_text_type}")
