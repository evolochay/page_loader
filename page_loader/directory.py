import os
from page_loader.naming import create_dir_name
from logs.log_config import logger


def make_path(path, file_name):
    return os.path.join(path, file_name)


def create_dir(dir_path, page_adress):
    dir_name = create_dir_name(page_adress)
    files_dir_path = make_path(dir_path, dir_name)
    try:
        os.mkdir(files_dir_path)
        return files_dir_path
    except FileExistsError as error:
        logger.error("File exist error:" f"{(error)}")
        raise error


def check_dir_access(dir_path):
    if not os.access(dir_path, os.R_OK & os.W_OK & os.X_OK):
        raise PermissionError("You may not use this directory")
    pass
