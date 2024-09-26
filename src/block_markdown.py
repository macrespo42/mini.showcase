def markdown_to_block(text: str) -> list[str]:
    blocks = text.split("\n\n")
    blocks = [block.strip() for block in blocks if block != ""]
    return blocks
