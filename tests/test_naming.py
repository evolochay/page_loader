from page_loader.naming import make_clear_url, make_url_with_scheme
from page_loader.naming import create_dir_name, create_file_name, create_page_name


URL_COURSES = "https://ru.hexlet.io/courses"
RAW = "tests/fixtures/raw.html"


def test_create_page_name():
    assert create_page_name("https://ru.hexlet.io/teams") == "ru-hexlet-io-teams.html"


def test_create_file_name():
    assert create_file_name("https://pythonist.ru/chto-vy-znaete-o-list-dict-comprehensions.jpg/") == "pythonist-ru-chto-vy-znaete-o-list-dict-comprehensions.jpg"


def test_create_dir_name():
    assert create_dir_name("https://ru.hexlet.io/courses") == "ru-hexlet-io-courses_files"


def test_clear_url():
    assert make_clear_url(URL_COURSES) == "https://ru.hexlet.io"


def test_check_http():
    assert make_url_with_scheme(URL_COURSES, RAW) == URL_COURSES + RAW
    assert make_url_with_scheme(RAW, URL_COURSES) == URL_COURSES
