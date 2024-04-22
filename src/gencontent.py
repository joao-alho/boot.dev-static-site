import os
from src.markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.strip().startswith("# "):
            return line[2:]
    raise Exception("H1 header not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:
        template = file.read()

    html_node = markdown_to_html_node(markdown)
    html_contents = html_node.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_contents)

    if not os.path.exists(dest_path):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        relative_content_path = os.path.join(dir_path_content, entry)
        dest_relative_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(relative_content_path) and entry.endswith(".md"):
            dest_path = dest_relative_path.replace(".md", ".html")
            generate_page(relative_content_path, template_path, dest_path)
        if os.path.isdir(relative_content_path):
            generate_pages_recursive(
                relative_content_path, template_path, dest_relative_path
            )
