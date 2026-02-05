# markdown_to_html.py (or wherever you keep your markdown pipeline)

from blocks import markdown_to_blocks, block_to_block_type, BlockType
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_to_textnodes, text_node_to_html_node


def text_to_children(text: str):
    """
    Convert inline-markdown text into a list of HTMLNodes.
    Uses your existing pipeline:
      text -> [TextNode] -> [HTMLNode]
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def paragraph_block_to_html_node(block: str):
    # Paragraphs can span multiple lines; join with spaces (matches your expected tests)
    joined = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(joined))


def heading_block_to_html_node(block: str):
    # block starts with 1-6 #'s then a space (already validated by block_to_block_type)
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1 :]  # skip the space after #'s
    return ParentNode(f"h{level}", text_to_children(text))


def code_block_to_html_node(block: str):
    # block format: ```\n ... \n```
    inner = block[4:-3]  # strip "```\n" and trailing "```"
    code = LeafNode("code", inner)
    return ParentNode("pre", [code])


def quote_block_to_html_node(block: str):
    # Remove leading '>' (space optional) from every line, then join with spaces
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        line = line[1:]  # remove leading ">"
        if line.startswith(" "):
            line = line[1:]
        cleaned.append(line)
    joined = " ".join(s.strip() for s in cleaned)
    return ParentNode("blockquote", text_to_children(joined))


def ul_block_to_html_node(block: str):
    items = []
    for line in block.split("\n"):
        text = line[2:]  # remove "- "
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ol_block_to_html_node(block: str):
    items = []
    for line in block.split("\n"):
        # remove "N. " where N increments; we can split once at ". "
        _, text = line.split(". ", 1)
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            children.append(paragraph_block_to_html_node(block))
        elif btype == BlockType.HEADING:
            children.append(heading_block_to_html_node(block))
        elif btype == BlockType.CODE:
            children.append(code_block_to_html_node(block))
        elif btype == BlockType.QUOTE:
            children.append(quote_block_to_html_node(block))
        elif btype == BlockType.UNORDERED_LIST:
            children.append(ul_block_to_html_node(block))
        elif btype == BlockType.ORDERED_LIST:
            children.append(ol_block_to_html_node(block))
        else:
            raise ValueError(f"Unknown block type: {btype}")

    return ParentNode("div", children)
