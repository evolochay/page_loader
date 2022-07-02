from tempfile import TemporaryDirectory
from main.loader import download, create_name
import requests_mock
from bs4 import BeautifulSoup


URL_COURSES = 'https://ru.hexlet.io/courses'
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_HTML = 'tests/fixtures/expected.html'



def read_file(file_path):
    with open(file_path, 'r') as file:
        result = file.read()
    return result


def test_create_file_name():
    result = create_name(URL_COURSES)
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
