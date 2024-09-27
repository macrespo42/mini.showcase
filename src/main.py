import os
import shutil

from block_markdown import extract_title, markdown_to_html_node


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


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    markdown_content = None
    template_content = None
    with open(from_path, "r") as markdown:
        markdown_content = markdown.read()
    with open(template_path, "r") as template:
        template_content = template.read()

    html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    print(html)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(template_content)


def main() -> None:
    clean_dir("./public")
    copy_dir("./static", "./public")
    generate_page("./content/index.md", "./template.html", "public/index.html")


if __name__ == "__main__":
    main()
