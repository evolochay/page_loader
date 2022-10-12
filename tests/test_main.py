import os
from bs4 import BeautifulSoup
from page_loader.page_loader import download
from page_loader.work_with_content import find_resources


HTML_WITH_LINKS = "tests/fixtures/html_with_links.html"
RAW = "tests/fixtures/raw.html"
IMG = "tests/fixtures/image.png"
HTML = "tests/fixtures/expected.html"
URL = "https://ru.hexlet.io"
CSS = "tests/fixtures/css_file.css"
JS = "tests/fixtures/js_file.js"
URL_IMG = "https://ru.hexlet.io/professions/python.png"
URL_CSS = "https://ru.hexlet.io/assets/application.css"
URL_JS = "https://ru.hexlet.io/packs/js/runtime.js"
DIRECTORY = "ru-hexlet-io_files"
EXPECTED_HTML = "ru-hexlet-io.html"
EXPECTED_IMG = os.path.join(DIRECTORY, "ru-hexlet-io-professions-python.png")
EXPECTED_CSS = os.path.join(DIRECTORY, "ru-hexlet-io-assets-application.css")
EXPECTED_JS = os.path.join(DIRECTORY, "ru-hexlet-io-packs-js-runtime.js")


def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()


def test_find_content(tmpdir):
    with open(HTML_WITH_LINKS, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), features="html.parser")
        all_resources, tag_lists = find_resources(soup, tmpdir, URL)
        for res in all_resources:
            print(res)
        assert len(all_resources) == 5
        assert len(tag_lists) == 5
