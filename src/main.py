from textnode import TextNode, TextType
from copy_dir import copy_dir_recursive
from generate import generate_page, generate_pages_recursive


def main():
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(text_node)

    copy_dir_recursive("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
