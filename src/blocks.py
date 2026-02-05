from enum import Enum, auto
import re


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    expected_num = 1
    ordered_ok = True
    for line in lines:
        prefix = f"{expected_num}. "
        if not line.startswith(prefix):
            ordered_ok = False
            break
        expected_num += 1
    if ordered_ok:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    if markdown == "":
        return []

    raw_blocks = re.split(r"\n\s*\n", markdown)

    blocks = []
    for b in raw_blocks:
        b = b.strip()
        if b != "":
            blocks.append(b)
    return blocks
