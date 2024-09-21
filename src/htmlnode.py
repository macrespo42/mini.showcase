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


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return self.value
        elif self.props is None or len(self.props) == 0:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
