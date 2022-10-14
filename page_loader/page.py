import requests
from logs.log_config import logger
from page_loader.naming import create_name
from page_loader.directory import make_path


def make_url_request(url):
    logger.info("Here is URL {}".format(url))
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error("problem with server`s response {}".format(url))
        raise error
    except requests.exceptions.Timeout as error:
        logger.error("Too long")
        raise error
    logger.info("Success {}".format(url))
    return response.content


def make_page_path(url, path):
    logger.info("path: {}".format(path))
    html_name = create_name(url, "page")
    page_path = make_path(path, html_name)
    return page_path


def write_data(file, data):
    try:
        with open(file, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise
