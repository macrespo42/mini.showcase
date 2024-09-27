from htmlnode import HTMLNode
from textnode import TextNode, text_type_text


def markdown_to_block(text: str) -> list[str]:
    blocks = text.split("\n\n")
    blocks = [block.strip() for block in blocks if block != ""]
    return blocks


def is_header(block: str) -> bool:
    if len(block) == 0:
        return False
    heading_level = 0
    if block[0] == "#":
        while heading_level < len(block) and block[heading_level] == "#":
            heading_level += 1
        if block[heading_level] != " " or heading_level > 6:
            return False
        else:
            return True
    else:
        return False


def is_code(block: str) -> bool:
    if len(block) < 6:
        return False
    if block[0:3] == "```" and block[-3:] == "```":
        lines = block.split("\n")
        for line in lines[1:-1]:
            if line[0] != ">":
                return False
        return True

    return False


def is_unordered_list(block: str) -> bool:
    if len(block) == 0:
        return False
    lines = block.split("\n")
    for line in lines:
        if len(line) < 2:
            return False
        if not (line[0:2] == "* " or line[0:2] == "- "):
            return False
    return True


def is_ordered_list(block: str) -> bool:
    if len(block) == 0:
        return False
    lines = block.split("\n")
    current_list_index = 0
    for line in lines:
        if len(line) < 2:
            return False
        if not (line[0].isnumeric() and line[1] == "."):
            return False
        if not (current_list_index + 1 == int(line[0])):
            return False
        current_list_index += 1
    return True


def block_to_block_type(block: str) -> str:
    if is_header(block):
        heading_level = 0
        while block[heading_level] == "#":
            heading_level += 1
        return f"h{heading_level}"
    elif is_code(block):
        return "code"
    elif is_unordered_list(block):
        return "ul"
    elif is_ordered_list(block):
        return "ol"
    else:
        return "p"


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_block(markdown)
    childrens = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_block = HTMLNode(
            tag=block_type,
            value=TextNode(block, text_type_text),
        )
        childrens.append(html_block)
    return HTMLNode("div", children=childrens)
