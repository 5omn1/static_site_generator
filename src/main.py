from textnode import TextNode, TextType
from copy_dir import copy_dir_recursive


def main():
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(text_node)
    copy_dir_recursive("static", "public")


if __name__ == "__main__":
    main()
