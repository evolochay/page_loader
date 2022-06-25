import os
from tempfile import TemporaryDirectory
from main.loader import download, get_page, create_file_name
import requests_mock


URL_COURSES = 'https://ru.hexlet.io/courses'
URL_Q = "https://ru.hexlet.io/qna"
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_HTML = 'tests/fixtures/expected.html'



def read_file(file_path):
    with open(file_path, 'r') as file:
        result = file.read()
    return result


def test_create_file_name():
    result = create_file_name(URL_COURSES)
    assert result == EXPECTED_FILE_NAME


def test_dowloads():
    with TemporaryDirectory() as test_dir:
        with requests_mock.Mocker() as mock:
            test_file = read_file(EXPECTED_HTML)
            mock.get(URL_Q, text = test_file)
            html_file_path = download(test_dir, URL_Q)
            file1 = read_file(html_file_path)
            assert test_file == file1
