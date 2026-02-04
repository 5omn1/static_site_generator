def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks
