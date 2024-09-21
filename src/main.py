from textnode import TextNode


def main() -> None:
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)


if __name__ == "__main__":
    main()
