import os
import htmlnode
from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            if title == "":
                raise Exception("H1 header found but title is empty")
            return title
    raise Exception("No H1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    content_html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
            continue
        if not entry.endswith(".md"):
            continue

        dest_path = dest_path[:-3] + ".html"
        generate_page(src_path, template_path, dest_path, basepath)
