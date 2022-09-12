import requests
from bs4 import BeautifulSoup
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
    except requests.exceptions.Timeout as exception:
        logger.error("Too long")
        raise exception
    logger.info("Success {}".format(url))
    return response.content


def download_page(url, path):
    logger.info("download html page: {}".format(url))
    html_name = create_name(url, "page")
    new_html = make_path(path, html_name)
    content = make_url_request(url)
    writing(new_html, content)
    return new_html


def writing(file, data):
    try:
        with open(file, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise


def get_soup(page_path):
    with open(page_path, "r", encoding='utf-8') as hp:
        soup = BeautifulSoup(hp.read(), "html.parser")
    return soup
