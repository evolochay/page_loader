from tempfile import TemporaryDirectory
from main.loader import download, create_name, find_domen_name
import requests_mock
import pytest
from bs4 import BeautifulSoup
import os


URL_COURSES = 'https://ru.hexlet.io/courses'
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_HTML = 'tests/fixtures/expected.html'
RAW = 'tests/fixtures/raw.html'
IMG = 'tests/fixtures/image.png'
HTML = 'tests/fixtures/expected2.html'
URL = 'https://ru.hexlet.io'
URL_IMG = 'https://ru.hexlet.io/professions/python.png'
DIRECTORY = 'ru-hexlet-io_files'
EXPECTED_HTML2 = 'ru-hexlet-io.html'
EXPECTED_IMG = "ru-hexlet-io_files/professions-python.png"


def read_file(file_path, binary=False):
    if not binary:
        with open(file_path, 'r') as f:
            return f.read()
    with open(file_path, 'rb') as file:
        return file.read()

@pytest.mark.parametrize(
    "test_case, expected, format",
    [
        (
            "https://ru.hexlet.io/teams",
            "ru-hexlet-io-teams.html",
            "page"
        ),
        (
            "https://ru.hexlet.io/courses",
            "ru-hexlet-io-courses_files",
            "directory"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions.jpg/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions-",
            "image"
        )
    ]
)
def test_create_name(test_case, expected, format):
    assert create_name(test_case, format) == expected


def test_create_file_name():
    result = create_name(URL_COURSES, 'page')
    assert result == EXPECTED_FILE_NAME


def test_dowloads():
    with TemporaryDirectory() as test_dir:
        with requests_mock.Mocker() as mock:
            test_file = read_file(EXPECTED_HTML)
            soup = BeautifulSoup(test_file, 'html.parser')
            mock.get(URL_Q, text = str(soup))
            html_file_path = download(test_dir, URL_Q)
            file1 = read_file(html_file_path)
            assert test_file == file1


def test_dowloads2():
    html_raw = read_file(RAW)
    html_expected = read_file(HTML)
    image = read_file(IMG, binary=True)

    with requests_mock.Mocker() as m, TemporaryDirectory() as tmpdir:
        m.get(URL, text=html_raw)
        m.get(URL_IMG, content=image)
        result = download(tmpdir, URL)
        print(result)

        html_path = os.path.join(tmpdir, EXPECTED_HTML2)
        img_path = os.path.join(tmpdir, EXPECTED_IMG)
        actual_html = read_file(html_path)
        assert actual_html == html_expected

        actual_img = read_file(img_path, binary=True)
        assert actual_img == image
        assert len(result) > 0


def test_find_domen_name():
    assert 'https://ru.hexlet.io' == find_domen_name(URL_COURSES)