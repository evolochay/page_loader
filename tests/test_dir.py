import os
import pytest
from page_loader.directory import make_path, create_dir
from page_loader.page_loader import download


URL_COURSES = "https://ru.hexlet.io/courses"


def test_make_path(tmpdir):
    file_name = "file_test_name"
    result = os.path.join(tmpdir, file_name)
    assert make_path(tmpdir, file_name) == result


def test_create_dir(tmpdir):
    dir_name = create_dir(tmpdir, URL_COURSES)
    assert len(dir_name) > 1
    with pytest.raises(FileExistsError):
        dir_name = create_dir(tmpdir, URL_COURSES)


def test_directory_doesnt_exist(tmpdir):
    nonexistent_directory = os.path.join(tmpdir, "something")
    with pytest.raises(PermissionError):
        download(URL_COURSES, nonexistent_directory)
