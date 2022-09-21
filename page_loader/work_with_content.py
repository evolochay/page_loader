from asyncio.log import logger
import requests
from urllib.parse import urljoin, urlparse
from progress.bar import Bar
from page_loader.naming import create_name, make_clear_url, check_http
from page_loader.directory import make_path
from page_loader.page import writing, make_url_request, get_soup

TAGS = {"img": "src", "link": "href", "script": "src"}


def download_content(page_url, page_path, dir_path, dir_name):
    soup = get_soup(page_path)
    resources = find_content(soup, page_url)
    clear_url = make_clear_url(page_url)
    count = len(resources)

    logger.info('I will download {} content links'.format(count))
    with Bar("Processing", max=count) as bar:
        for res in resources:
            source_atr = TAGS[res.name]
            res_url = urljoin(page_path, res[source_atr])
            content_url = check_http(clear_url, res_url)
            res_name = create_name(content_url, "file")
            try:
                res_path = make_path(dir_path, res_name)
                content = make_url_request(content_url)
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
                                   compare_host_name(res[TAGS[res.name]],
                                                    url),
                                   sum(all_resources, [])))
    return filter_resources


def compare_host_name(url, parent_url):
    url_domain = urlparse(url).netloc
    same_domain_name = urlparse(url).netloc != urlparse(parent_url).netloc
    print(same_domain_name)
    return not (url_domain and same_domain_name)
