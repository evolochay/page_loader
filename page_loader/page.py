import requests
from logs.log_config import logger
from page_loader.naming import create_name
from page_loader.directory import make_path


def make_url_request(url, bytes=False):
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
    return check_bytes(response, bytes)


def check_bytes(response, bytes):
    if bytes is True:
        return response.content
    else:
        return response.text


def download_page(url, path, get_content=make_url_request):
    logger.info("download html page: {}".format(url))
    html_name = create_name(url, "page")
    new_html = make_path(path, html_name)
    content = get_content(url)
    writing(new_html, content)
    return new_html


def writing(file, data, bytes=False):
    if bytes is True:
        tag = "wb"
    else:
        tag = "w"
    with open(file, tag) as f:
        f.write(data)
