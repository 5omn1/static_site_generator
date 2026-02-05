import unittest
from generate import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_extract_title_first_h1_only(self):
        md = "# First\n\n# Second"
        self.assertEqual(extract_title(md), "First")

    def test_extract_title_ignores_h2(self):
        md = "## Not it\n\n### Also not it"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_raises_if_missing(self):
        md = "No headings here"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_raises_if_empty_title(self):
        md = "#   \n\nstuff"
        with self.assertRaises(Exception):
            extract_title(md)
