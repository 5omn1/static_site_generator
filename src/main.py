import sys
from copy_dir import copy_dir_recursive
from generate import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"

    output_dir = "docs"

    copy_dir_recursive("static", output_dir)

    generate_pages_recursive("content", "template.html", output_dir, basepath)


if __name__ == "__main__":
    main()
