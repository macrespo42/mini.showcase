import os
import shutil
from pathlib import Path

from block_markdown import extract_title, markdown_to_html_node

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def clean_dir(path: str) -> None:
    files = os.listdir(path)
    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            print(f"Deleting file: {full_path}")
            os.unlink(full_path)
        elif os.path.isdir(full_path):
            print(f"Deleting directory: {full_path}")
            shutil.rmtree(full_path)


def copy_dir(src: str, dst: str) -> None:
    if not (os.path.exists(src) and os.path.exists(dst)):
        raise ValueError("Path does not exist")

    to_copy = os.listdir(src)
    for file in to_copy:
        full_path = os.path.join(src, file)
        if os.path.isfile(full_path):
            full_dst = os.path.join(dst, file)
            print(f"Copying {full_path} to {full_dst}")
            shutil.copy(full_path, full_dst)
        elif os.path.isdir(full_path):
            full_dst = os.path.join(dst, file)
            os.mkdir(full_dst)
            copy_dir(full_path, full_dst)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def main() -> None:
    clean_dir(dir_path_public)
    copy_dir(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
