from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


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
    lines = block.split("\n")
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
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


def is_blockquote(block: str) -> bool:
    lines = block.split("\n")
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return False
        return True


def block_to_block_type(block: str) -> str:
    if is_header(block):
        return "h"
    elif is_code(block):
        return "code"
    elif is_blockquote(block):
        return "blockquote"
    elif is_unordered_list(block):
        return "ul"
    elif is_ordered_list(block):
        return "ol"
    else:
        return "p"


def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def header_to_html_node(block: str) -> ParentNode:
    header_level = 0
    while block[header_level] == "#":
        header_level += 1
    if header_level + 1 > len(block):
        raise ValueError("Invalid block: header level to high")
    children = text_to_children(block[header_level + 1 :])
    return ParentNode(f"h{header_level}", children)


def code_to_html_node(block: str) -> ParentNode:
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def unordered_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        li_child = text_to_children(line[2:])
        children.append(ParentNode("li", li_child))
    return ParentNode("ul", children)


def ordered_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    children = []
    for line in lines:
        li_child = text_to_children(line[3:])
        children.append(ParentNode("li", li_child))
    return ParentNode("ol", children)


def blockquote_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == "p":
        return paragraph_to_html_node(block)
    elif block_type == "h":
        return header_to_html_node(block)
    elif block_type == "code":
        return code_to_html_node(block)
    elif block_type == "ul":
        return unordered_list_to_html(block)
    elif block_type == "ol":
        return ordered_list_to_html(block)
    elif block_type == "blockquote":
        return blockquote_to_html(block)
    else:
        raise ValueError("Invalid block: block type not found")


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_block(markdown)
    childrens = []
    for block in blocks:
        node = block_to_html_node(block)
        childrens.append(node)
    return ParentNode("div", children=childrens)


def extract_title(markdown: str):
    blocks = markdown_to_block(markdown)
    header = blocks[0]
    if not header.startswith("# "):
        raise ValueError("Invalid markdown: the file doesn't start with a title")
    return header.lstrip("#").strip()
