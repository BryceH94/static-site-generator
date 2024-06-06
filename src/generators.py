from converters import markdown_to_html_node
from htmlnode import HTMLNode
from extractors import extract_title
from os import path, makedirs, listdir 

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_content = f.read()
    with open(template_path, "r") as f:
        dest_html = f.read()
    from_html = markdown_to_html_node(from_content).to_html()
    from_title = extract_title(from_content)
    dest_html = dest_html.replace(r"{{ Title }}", from_title)
    dest_html = dest_html.replace(r"{{ Content }}", from_html)
    makedirs(path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(dest_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = listdir(dir_path_content)
    for item in items:
        if path.isfile(path.join(dir_path_content, item)):
            if item.endswith(".md"):
                generate_page(path.join(dir_path_content, item), template_path, path.join(dest_dir_path, item.replace(".md", ".html")))
        else:
            generate_pages_recursive(path.join(dir_path_content, item), template_path, path.join(dest_dir_path, item))
        