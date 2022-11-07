import os
import pytest
from page_loader.os_data import create_dir
from page_loader.page_loader import download


URL_COURSES = "https://ru.hexlet.io/courses"


def test_create_dir(tmpdir):
    dir_name = create_dir(tmpdir, URL_COURSES)
    assert len(dir_name) > 1
    with pytest.raises(FileExistsError):
        dir_name = create_dir(tmpdir, URL_COURSES)


def test_directory_doesnt_exist(tmpdir):
    nonexistent_directory = os.path.join(tmpdir, "something")
    with pytest.raises(PermissionError):
        download(URL_COURSES, nonexistent_directory)
