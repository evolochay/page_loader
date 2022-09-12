import tempfile
import requests_mock
import pytest
import os
import requests
from page_loader.page_loader import download
from page_loader.page import make_url_request, download_page
from page_loader.naming import create_name
from page_loader.directory import make_path, create_dir


URL_COURSES = "https://ru.hexlet.io/courses"
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = "ru-hexlet-io-courses.html"
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
INVALID_URL = "htps://ru.hexlet.io/courses"


def test_directory_doesnt_exist():
    with tempfile.TemporaryDirectory() as tmpdirname:
        nonexistent_directory = os.path.join(tmpdirname, "something")
        with pytest.raises(UnboundLocalError):
            download(URL_COURSES, nonexistent_directory)


def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()


@pytest.mark.parametrize(
    "test_case, expected, ext",
    [
        ("https://ru.hexlet.io/teams", "ru-hexlet-io-teams.html", "page"),
        ("https://ru.hexlet.io/courses", "ru-hexlet-io-courses_files", "dir"),
        (
            "https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions.jpg/",
            "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.jpg",
            "file",
        ),
    ],
)
def test_create_name(test_case, expected, ext):
    assert create_name(test_case, ext) == expected


def test_make_url_request():
    with requests_mock.Mocker() as m:
        m.get(
            INVALID_URL,
            content=read_file("tests/fixtures/test_file.txt"),
            status_code=200,
        )
        result = make_url_request(INVALID_URL)
        assert result == b"Just file for test"


def test_connection_error(requests_mock):
    invalid_url = "https://badsite.com"
    requests_mock.get(invalid_url, exc=requests.exceptions.ConnectionError)
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)
        with pytest.raises(Exception):
            assert download(invalid_url, tmpdirname)
        assert not os.listdir(tmpdirname)


@pytest.mark.parametrize("wrong_url", INVALID_URL)
def test_download_page2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(Exception):
            download_page(wrong_url, d)


def test_make_path():
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_name = "file_test_name"
        result = os.path.join(tmpdirname, file_name)
        assert make_path(tmpdirname, file_name) == result


def fake_data(*args):
    return "hello"


def test_download_page1():
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, EXPECTED_FILE_NAME)
        new_html = download_page(URL_COURSES, d)
        assert os.path.exists(new_html)
        assert new_html == path_file


def test_create_dir():
    with tempfile.TemporaryDirectory() as d:
        dir_name, dir = create_dir(d, URL_COURSES)
        assert os.path.exists(dir)
        assert len(dir_name) > 1


@pytest.mark.parametrize("code", [500, 400, 404])
def test_http_errors(code):
    with requests_mock.Mocker() as m:
        m.get(
            INVALID_URL,
            content=read_file("tests/fixtures/test_file.txt"),
            status_code=code,
        )
        with pytest.raises(requests.exceptions.HTTPError):
            make_url_request(INVALID_URL)


def test_with_timeout():
    with requests_mock.Mocker() as m:
        m.get(URL, exc=requests.Timeout)
        with pytest.raises(requests.exceptions.Timeout):
            make_url_request(URL)


@pytest.fixture()
def test_dowloads(tmpdir, requests_mock):
    html_raw = read_file(RAW)
    html_expected = read_file(HTML)
    image = read_file(IMG)
    css = read_file(CSS)
    js = read_file(JS)

    requests_mock.get(URL, content=html_raw)
    requests_mock.get(URL_IMG, content=image)
    requests_mock.get(URL_CSS, content=css)
    requests_mock.get(URL_JS, content=js)
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
