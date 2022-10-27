import os
import requests
import pytest
from page_loader.page import get_page_content, make_page_path
from page_loader.page_loader import download
from tests.test_main import read_file


EXPECTED_FILE_NAME = "ru-hexlet-io-courses.html"
URL_COURSES = "https://ru.hexlet.io/courses"
INVALID_URL = "htps://ru.hexlet.io/courses"
URL = "https://ru.hexlet.io"


def test_download_page1(tmpdir):
    path_file = os.path.join(tmpdir, EXPECTED_FILE_NAME)
    new_html = make_page_path(URL_COURSES, tmpdir)
    assert new_html == path_file


def test_make_url_request(requests_mock):
    requests_mock.get(
        INVALID_URL,
        content=read_file("tests/fixtures/test_file.txt"),
        status_code=200,
    )
    result = get_page_content(INVALID_URL)
    assert result == b"Just file for test"


def test_with_timeout(requests_mock, tmpdir):
    requests_mock.get(URL, exc=requests.exceptions.Timeout)
    with pytest.raises(requests.exceptions.Timeout):
        get_page_content(URL)
        download(URL, tmpdir)
