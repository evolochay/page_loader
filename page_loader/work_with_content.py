from asyncio.log import logger
import requests
from urllib.parse import urljoin, urlparse
from progress.bar import Bar
from page_loader.naming import create_name, make_clear_url, make_url_with_scheme
from page_loader.directory import make_path
from page_loader.page import write_data, make_url_request

TAGS = {"img": "src", "link": "href", "script": "src"}


def download_content(page_url, page_path, dir_path, dir_name, resources):
    clear_url = make_clear_url(page_url)
    count = len(resources)

    logger.info('I will download {} content links'.format(count))
    with Bar("Processing", max=count) as bar:
        for res in resources:
            source_atr = TAGS[res.name]
            res_url = urljoin(page_path, res[source_atr])
            content_url = make_url_with_scheme(clear_url, res_url)
            res_name = create_name(content_url, "file")
            try:
                res_path = make_path(dir_path, res_name)
                content = make_url_request(content_url)
                write_data(res_path, content)
            except (PermissionError, requests.RequestException) as e:
                logger.warning(e)
                logger.warning('I can not download {}'.format(res_name))
                pass
            else:
                res[source_atr] = make_path(dir_name, res_name)
            bar.next()


def update_html(page_path, soup):
    with open(page_path, 'w') as hp:
        hp.write(soup.prettify())


def find_resources(soup, url):
    all_resources = list(map(lambda tag, atr:
                             soup.find_all(tag, attrs={atr: True}),
                             TAGS.keys(), TAGS.values()))
    filter_resources = list(filter(lambda res:
                                   compare_host_name(res[TAGS[res.name]],
                                                     url),
                                   sum(all_resources, [])))
    print(filter_resources)
    return filter_resources


def compare_host_name(url, parent_url):
    url_domain = urlparse(url).netloc
    same_domain_name = urlparse(url).netloc != urlparse(parent_url).netloc
    return not (url_domain and same_domain_name)
