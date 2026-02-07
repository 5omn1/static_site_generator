from blocks import markdown_to_blocks, block_to_block_type, BlockType
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_to_text_nodes, text_node_to_html_node


def text_to_children(text: str):
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def paragraph_block_to_html_node(block: str):
    joined = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(joined))


def heading_block_to_html_node(block: str):
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_block_to_html_node(block: str):
    inner = block[4:-3]
    code = LeafNode("code", inner)
    return ParentNode("pre", [code])


def quote_block_to_html_node(block: str):
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        line = line[1:]
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
