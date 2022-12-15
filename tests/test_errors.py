import pytest
import requests
import os
from page_loader.user_messages import Message
from page_loader.page_loader import download
from tests.test_main import read_file
from page_loader.io import get_page_content


INVALID_URL = "htps://ru.hexlet.io/courses"


@pytest.mark.parametrize(
    "problem_name, message",
    [
        (Message.CONNECTION_ERROR, "Please, check Internet connection"),
        (Message.HTTP_ERROR, "You`ve got some problem with HTTP"),
        (Message.PERMISSION_DENIED, "You can not use this directory"),
        (Message.UNEXPECTED, "We don`t know, what is wrong"),
        (Message.TIMEOUT, "We are waiting too long")])
def test_create_errors_message(problem_name, message):
    assert problem_name.value == message


def test_connection_error(requests_mock, tmpdir):
    invalid_url = "https://badsite.com"
    requests_mock.get(invalid_url, exc=requests.exceptions.ConnectionError)
    assert not os.listdir(tmpdir)
    with pytest.raises(Exception):
        assert download(invalid_url, tmpdir)
    assert not os.listdir(tmpdir)


@pytest.mark.parametrize("code", [500, 400, 404])
def test_http_errors(code, requests_mock):
    requests_mock.get(
        INVALID_URL,
        content=read_file("tests/fixtures/test_file.txt"),
        status_code=code,
    )
    with pytest.raises(requests.exceptions.HTTPError):
        get_page_content(INVALID_URL)
