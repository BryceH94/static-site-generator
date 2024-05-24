import unittest

from extractors import extract_markdown_images
from extractors import extract_markdown_links

class TestExtractMarkdownImages(unittest.TestCase):
    def test_two_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_result = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    if __name__ == "__main__":
        unittest.main()

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_two_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), expected_result)

    if __name__ == "__main__":
        unittest.main()

