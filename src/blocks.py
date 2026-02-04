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
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks
