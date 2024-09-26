import re

from textnode import TextNode, text_type_image, text_type_link, text_type_text


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
        return new_nodes


def extract_markdown_images(text: str):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images


def extract_markdown_links(text: str):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, formatted section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, formatted section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes


if __name__ == "__main__":
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type_text,
    )
    print(split_nodes_link([node]))
