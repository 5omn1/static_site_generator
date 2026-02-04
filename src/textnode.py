from enum import Enum, auto
from leafnode import LeafNode
import re


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
