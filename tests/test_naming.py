import pytest
from page_loader.naming import make_clear_url, check_http, create_name


URL_COURSES = "https://ru.hexlet.io/courses"
RAW = "tests/fixtures/raw.html"


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


def test_clear_url():
    assert make_clear_url(URL_COURSES) == "https://ru.hexlet.io"



def test_check_http():
    assert check_http(URL_COURSES, RAW) == URL_COURSES + RAW
    assert check_http(RAW, URL_COURSES) == URL_COURSES
