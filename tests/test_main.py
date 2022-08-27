from tempfile import TemporaryDirectory
import tempfile
from page_loader.page_loader import download
from page_loader.functions import create_name, make_url_request, writing, download_page
from page_loader.functions import make_path, create_dir
import requests_mock
from requests_mock import mock
import pytest
import os
import requests


URL_COURSES = 'https://ru.hexlet.io/courses'
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'
RAW = 'tests/fixtures/raw.html'
IMG = 'tests/fixtures/image.png'
HTML = 'tests/fixtures/expected.html'
URL = 'https://ru.hexlet.io'
CSS = 'tests/fixtures/css_file.css'
JS = 'tests/fixtures/js_file.js'
URL_IMG = 'https://ru.hexlet.io/professions/python.png'
URL_CSS = 'https://ru.hexlet.io/assets/application.css'
URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'
DIRECTORY = 'ru-hexlet-io_files'
EXPECTED_HTML = 'ru-hexlet-io.html'
EXPECTED_IMG = os.path.join(DIRECTORY, 'ru-hexlet-io-professions-python.png')
EXPECTED_CSS = os.path.join(DIRECTORY, 'ru-hexlet-io-assets-application.css')
EXPECTED_JS = os.path.join(DIRECTORY, 'ru-hexlet-io-packs-js-runtime.js')
INVALID_URL = 'htps://ru.hexlet.io/courses'


def test_directory_doesnt_exist():
    with tempfile.TemporaryDirectory() as tmpdirname:
        nonexistent_directory = os.path.join(tmpdirname, 'something')
        with pytest.raises(UnboundLocalError):
            download(URL_COURSES, nonexistent_directory)


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


@pytest.mark.parametrize(
    "test_case, expected, ext",
    [
        (
            "https://ru.hexlet.io/teams",
            "ru-hexlet-io-teams.html",
            "page"
        ),
        (
            "https://ru.hexlet.io/courses",
            "ru-hexlet-io-courses_files",
            "dir"
        ),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions.jpg/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.jpg",
            'file'
        )
    ]
)
def test_create_name(test_case, expected, ext):
    assert create_name(test_case, ext) == expected


def test_dowloads():
    html_raw = read_file(RAW)
    html_expected = read_file(HTML)
    image = read_file(IMG)
    css = read_file(CSS)
    js = read_file(JS)

    with requests_mock.Mocker() as m, TemporaryDirectory() as tmpdir:
        m.get(URL, content=html_raw)
        m.get(URL_IMG, content=image)
        m.get(URL_CSS, content=css)
        m.get(URL_JS, content=js)
        result = download(URL, tmpdir)

        html_path = os.path.join(tmpdir, EXPECTED_HTML)
        img_path = os.path.join(tmpdir, EXPECTED_IMG)
        css_path = os.path.join(tmpdir, EXPECTED_CSS)
        js_path = os.path.join(tmpdir, EXPECTED_JS)

        actual_html = read_file(html_path)
        assert actual_html == html_expected

        actual_img = read_file(img_path)
        assert actual_img == image

        actual_css = read_file(css_path)
        assert actual_css == css

        actual_js = read_file(js_path)
        assert actual_js == js

        assert len(result) > 0


def test_make_url_request():
    with mock() as m:
        m.get(INVALID_URL, text=open('tests/fixtures/test_file.txt', 'r').read(), status_code=200)
        result = make_url_request(INVALID_URL)
        assert result == 'Just file for test'


def test_connection_error(requests_mock):
    invalid_url = 'https://badsite.com'
    requests_mock.get(invalid_url, exc=requests.exceptions.ConnectionError)
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)
        with pytest.raises(Exception):
            assert download(invalid_url, tmpdirname)
        assert not os.listdir(tmpdirname)


def test_writing_text():
    data = 'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, 'new_file.html')
        writing(path_file, data)
        with open(path_file, 'r') as f:
            assert data == f.read()


@pytest.mark.parametrize('wrong_url', INVALID_URL)
def test_download_page2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(Exception):
            download_page(wrong_url, d)


def test_make_path():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = 'file_test_name'
        result = os.path.join(tmpdirname, file_name)
        assert make_path(tmpdirname, file_name) == result


def fake_data(*args):
    return 'hello'


def test_download_page1():
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, EXPECTED_FILE_NAME)
        new_html = download_page(URL_COURSES, d, get_content=fake_data)
        assert os.path.exists(new_html)
        assert new_html == path_file


def test_create_dir():
    with tempfile.TemporaryDirectory() as d:
        dir = create_dir(d, URL_COURSES)
        assert os.path.exists(dir)
