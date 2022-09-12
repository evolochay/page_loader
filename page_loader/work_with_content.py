from asyncio.log import logger
import requests
from urllib.parse import urljoin, urlparse
from progress.bar import Bar
from page_loader.naming import create_name
from page_loader.directory import make_path
from page_loader.page import writing, make_url_request

TAGS = {"img": "src", "link": "href", "script": "src"}


def download_content(resource_dict, page_path, dir_path, dir_name, soup, clear_url):
    count = len(resource_dict)
    logger.info('page path{}'.format(page_path))
    logger.info('dir path{}'.format(dir_path))
    logger.info('dir name{}'.format(dir_name))
    logger.info('I will download {} content links'.format(count))
    with Bar("Processing", max=count) as bar:
        for res in resource_dict:
            source_atr = TAGS[res.name]
            res_url = urljoin(page_path, res[source_atr])
            res_name = create_name(res_url, "file")
            try:
                res_path = make_path(dir_path, res_name)
                content = make_url_request(clear_url + "/" + res_url)
                writing(res_path, content)
            except (PermissionError, requests.RequestException) as e:
                logger.error(e)
                logger.warning('I can not download {}'.format(res_name))
                pass
            else:
                res[source_atr] = make_path(dir_name, res_name)
            bar.next()
            save_html_changes(page_path, soup)


def save_html_changes(page_path, soup):
    with open(page_path, 'w') as hp:
        hp.write(soup.prettify())


def find_content(soup, url):
    all_resources = list(map(lambda tag, atr:
                             soup.find_all(tag, attrs={atr: True}),
                             TAGS.keys(), TAGS.values()))
    filter_resources = list(filter(lambda res:
                                   check_parent_url(res[TAGS[res.name]],
                                                    url),
                                   sum(all_resources, [])))
    return filter_resources


def check_parent_url(url, parent_url):
    domen1 = urlparse(url).netloc
    domen2 = urlparse(url).netloc != urlparse(parent_url).netloc
    return not(domen1 and domen2)
