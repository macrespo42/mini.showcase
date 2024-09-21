from typing import Any


class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list[Any] = None,
        props: dict = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = []
        for key, value in self.props.items():
            html.append(f'{key}="{value}"')
        return " ".join(html)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
