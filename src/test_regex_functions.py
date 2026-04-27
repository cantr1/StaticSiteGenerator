import unittest

from helper_functions import extract_markdown_links, extract_markdown_images

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links_from_markdown(self):
        text = "This is a [link](https://www.example.com) in markdown."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]["anchor_text"], "link")
        self.assertEqual(links[0]["url"], "https://www.example.com")

    def test_extract_links_from_markdown_multiple(self):
        text = "This is a [link](https://www.example.com) and another [link2](https://www.example2.com) in markdown."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]["anchor_text"], "link")
        self.assertEqual(links[0]["url"], "https://www.example.com")
        self.assertEqual(links[1]["anchor_text"], "link2")
        self.assertEqual(links[1]["url"], "https://www.example2.com")

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images_from_markdown(self):
        text = "This is an image: ![alt text](https://www.example.com/image.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]["alt_text"], "alt text")
        self.assertEqual(images[0]["url"], "https://www.example.com/image.jpg")

    def test_extract_images_from_markdown_multiple(self):
        text = "This is an image: ![alt text](https://www.example.com/image.jpg) and another ![alt2](https://www.example2.com/image2.jpg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0]["alt_text"], "alt text")
        self.assertEqual(images[0]["url"], "https://www.example.com/image.jpg")
        self.assertEqual(images[1]["alt_text"], "alt2")
        self.assertEqual(images[1]["url"], "https://www.example2.com/image2.jpg")