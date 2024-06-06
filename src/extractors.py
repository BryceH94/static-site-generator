import re

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    
def extract_markdown_links(text):
    return [(match[1], match[2]) for match in re.findall(r"(^|\s)\[(.*?)\]\((.*?)\)",text)]

def extract_title(markdown):
    title = markdown.split("\n", maxsplit=1)[0]
    if title:
        if title.startswith("# "):
            return title[2:].strip()
        else:
            raise Exception("No title provided")
    else:
        raise Exception("No text provided")