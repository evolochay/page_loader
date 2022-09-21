import pytest
import os
import requests
from bs4 import BeautifulSoup
from page_loader.page_loader import download
from page_loader.page import make_url_request, download_page
from page_loader.directory import make_path, create_dir
from page_loader.naming import make_clear_url, check_http, create_name
from page_loader.user_messages import create_errors_message
from page_loader.work_with_content import find_content


URL_COURSES = "https://ru.hexlet.io/courses"
URL_Q = "https://quotes.toscrape.com"
EXPECTED_FILE_NAME = "ru-hexlet-io-courses.html"
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
INVALID_URL = "htps://ru.hexlet.io/courses"


@pytest.mark.parametrize(
    "problem_name, message",
    [
        ("connection error", "Please, check Internet connection"),
        ("HTTP error", "You`ve got some problem with HTTP"),
        ("permission denied", "You can not use this directory"),
        ("unexpected_err", "We don`t know, what is wrong"),
        ("timeout", "We are waiting too long")])
def test_create_errors_message(problem_name, message):
    assert create_errors_message(problem_name) == message


def test_directory_doesnt_exist(tmpdir):
    nonexistent_directory = os.path.join(tmpdir, "something")
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


def test_make_url_request(requests_mock):
    requests_mock.get(
        INVALID_URL,
        content=read_file("tests/fixtures/test_file.txt"),
        status_code=200,
    )
    result = make_url_request(INVALID_URL)
    assert result == b"Just file for test"


def test_connection_error(requests_mock, tmpdir):
    invalid_url = "https://badsite.com"
    requests_mock.get(invalid_url, exc=requests.exceptions.ConnectionError)
    assert not os.listdir(tmpdir)
    with pytest.raises(Exception):
        assert download(invalid_url, tmpdir)
    assert not os.listdir(tmpdir)


@pytest.mark.parametrize("wrong_url", INVALID_URL)
def test_download_page2(wrong_url, tmpdir):
    with pytest.raises(Exception):
        download_page(wrong_url, tmpdir)


def test_make_path(tmpdir):
    file_name = "file_test_name"
    result = os.path.join(tmpdir, file_name)
    assert make_path(tmpdir, file_name) == result


def test_download_page1(tmpdir):
    path_file = os.path.join(tmpdir, EXPECTED_FILE_NAME)
    new_html = download_page(URL_COURSES, tmpdir)
    assert os.path.exists(new_html)
    assert new_html == path_file


def test_create_dir(tmpdir):
    dir_name, dir = create_dir(tmpdir, URL_COURSES)
    assert os.path.exists(dir)
    assert len(dir_name) > 1
    with pytest.raises(FileExistsError):
        dir_name, dir = create_dir(tmpdir, URL_COURSES)


@pytest.mark.parametrize("code", [500, 400, 404])
def test_http_errors(code, requests_mock):
    requests_mock.get(
        INVALID_URL,
        content=read_file("tests/fixtures/test_file.txt"),
        status_code=code,
    )
    with pytest.raises(requests.exceptions.HTTPError):
        make_url_request(INVALID_URL)


def test_with_timeout(requests_mock, tmpdir):
    requests_mock.get(URL, exc=requests.exceptions.Timeout)
    with pytest.raises(requests.exceptions.Timeout):
        make_url_request(URL)
        download(URL, tmpdir)


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


def test_clear_url():
    assert make_clear_url(URL_COURSES) == "https://ru.hexlet.io"


def test_check_http():
    assert check_http(URL_COURSES, RAW) == URL_COURSES + RAW
    assert check_http(RAW, URL_COURSES) == URL_COURSES


def test_find_content():
    with open(HTML_WITH_LINKS, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), features="html.parser")
        all_resources = find_content(soup, URL)
        assert len(all_resources) == 5
