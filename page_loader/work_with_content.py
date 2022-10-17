from asyncio.log import logger
import os
import requests
from progress.bar import Bar
from urllib.parse import urljoin, urlparse
from page_loader.naming import create_file_name
from page_loader.directory import make_path
from page_loader.classes import Tag, Resourse


RESOURCE_TAGS = {"img": "src", "link": "href", "script": "src"}


def find_resources(soup, dir_path, url):
    tags = RESOURCE_TAGS.keys()
    resource_tags = soup.find_all(tags)
    filter_resources = []
    tags_list = []
    for res in resource_tags:
        logger.info(res)
        attr = RESOURCE_TAGS[res.name]
        attr_value = res.get(attr)
        if not is_same_host_name(attr_value, url):
            continue
        resource_url = urljoin(url, attr_value).rstrip("/")
        resource_name = create_file_name(resource_url)
        logger.info("Resource name: {}".format(resource_name))
        resource_path = make_path(dir_path, resource_name)
        new_attr_value = os.path.join(
            os.path.basename(dir_path), resource_name)
        filter_resources.append(Resourse(resource_url, resource_path))
        tags_list.append(Tag(res, attr, new_attr_value))
    logger.info('I found {} res'.format(len(filter_resources)))
    return filter_resources, tags_list


def download_content(resources):
    count = len(resources)
    logger.info('I will download {} content links'.format(count))
    with Bar("Processing", max=count) as bar:
        for res in resources:
            try:
                get_web_resource(
                    res.resource_url, res.resource_path)
                bar.next()
            except (PermissionError, requests.RequestException) as e:
                logger.warning(e)
                logger.warning('Сan`t download {}'.format(res['resource_url']))
                pass
        bar.finish()


def is_same_host_name(url, parent_url):
    url_domain = urlparse(url).netloc
    is_same_domain_name = urlparse(url).netloc != urlparse(parent_url).netloc
    return not (url_domain and is_same_domain_name)


def get_web_resource(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1000):
            file.write(chunk)


def replace_res_path(tags):
    for tag in tags:
        new_tag = tag.tag
        new_tag[tag.attr] = tag.new_attr_value
