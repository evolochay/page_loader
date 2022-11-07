import requests
from logs.log_config import logger


def get_page_content(url):
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


def get_web_resource(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1000):
            file.write(chunk)
