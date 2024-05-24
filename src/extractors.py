import re

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    
def extract_markdown_links(text):
    # Currently would also match on images
    # Will have to see how it's used in the course and adjust, if needed
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)