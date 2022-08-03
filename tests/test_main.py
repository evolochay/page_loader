from cgitb import reset
from tempfile import TemporaryDirectory
from page_loader.loader import download, create_name, find_domen_name, make_url_request
import requests_mock
import pytest
import os


URL_COURSES = 'https://ru.hexlet.io/courses'
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_HTML = 'tests/fixtures/expected.html'
RAW = 'tests/fixtures/raw.html'
IMG = 'tests/fixtures/image.png'
HTML = 'tests/fixtures/expected2.html'
URL = 'https://ru.hexlet.io'
CSS = 'tests/fixtures/css_file.css'
JS = 'tests/fixtures/js_file.js'
URL_IMG = 'https://ru.hexlet.io/professions/python.png'
URL_CSS = 'https://ru.hexlet.io/assets/application.css'
URL_JS = 'https://ru.hexlet.io/packs/js/runtime.js'
DIRECTORY = 'ru-hexlet-io_files'
EXPECTED_HTML2 = 'ru-hexlet-io.html'
EXPECTED_IMG = os.path.join(DIRECTORY, 'ru-hexlet-io-professions-python.png')
EXPECTED_CSS = os.path.join(DIRECTORY, 'ru-hexlet-io-assets-application.css')
EXPECTED_JS = os.path.join(DIRECTORY, 'ru-hexlet-io-packs-js-runtime.js')
INVALID_URL = 'htps://ru.hexlet.io/courses'


def read_file(file_path, binary=False):
    print(file_path)
    if not binary:
        with open(file_path, 'r') as f:
            return f.read()
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


def test_create_file_name():
    result = create_name(URL_COURSES, 'page')
    assert result == EXPECTED_FILE_NAME


def test_dowloads2():
    html_raw = read_file(RAW)
    html_expected = read_file(HTML)
    image = read_file(IMG, binary=True)
    css = read_file(CSS, binary=True)
    js = read_file(JS, binary=True)

    with requests_mock.Mocker() as m, TemporaryDirectory() as tmpdir:
        m.get(URL, text=html_raw)
        m.get(URL_IMG, content=image)
        m.get(URL_CSS, content=css)
        m.get(URL_JS, content=js)
        result = download(tmpdir, URL)
        print(result)

        html_path = os.path.join(tmpdir, EXPECTED_HTML2)
        img_path = os.path.join(tmpdir, EXPECTED_IMG)
        css_path = os.path.join(tmpdir, EXPECTED_CSS)
        js_path = os.path.join(tmpdir, EXPECTED_JS)

        actual_html = read_file(html_path)
        assert actual_html == html_expected

        actual_img = read_file(img_path, binary=True)
        assert actual_img == image

        actual_css = read_file(css_path, binary=True)
        assert actual_css == css

        actual_js = read_file(js_path, binary=True)
        assert actual_js == js

        assert len(result) > 0


def test_find_domen_name():
    assert 'https://ru.hexlet.io' == find_domen_name(URL_COURSES)


def test_make_url_request():
    with requests_mock.Mocker() as m:
        m.get(INVALID_URL, text=open('tests/fixtures/test_file.txt', 'r').read(), status_code=200)
        result = make_url_request(INVALID_URL).text
        assert result == 'Just file for test'


def test_make_url_request2():
    with requests_mock.Mocker() as m:
       m.get(INVALID_URL, text=open('tests/fixtures/test_file.txt', 'r').read(), status_code=500)
       with pytest.raises(SystemExit):
            make_url_request(INVALID_URL)
