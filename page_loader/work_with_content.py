from asyncio.log import logger
import os
import requests
from urllib.parse import urljoin, urlparse
from progress.bar import Bar
from page_loader.naming import create_name
from page_loader.directory import make_path


TAGS = {"img": "src", "link": "href", "script": "src"}


def find_resources(soup, dir_path, url):
    logger.info("HERE IN FIND")
    tags = TAGS.keys()
    resource_tags = soup.find_all(tags)
    filter_resources = []
    tags_list = []
    for res in resource_tags:
        logger.info(res)
        attr = TAGS[res.name]
        attr_value = res.get(attr)
        if not compare_host_name(attr_value, url):
            continue
        resource_url = urljoin(url, attr_value).rstrip("/")
        resource_name = create_name(resource_url, "file")
        logger.info("Resource name: {}".format(resource_name))
        resource_path = make_path(dir_path, resource_name)
        new_attr_value = os.path.join(
            os.path.basename(dir_path), resource_name)

        filter_resources.append(
            {
                'resource_url': resource_url,
                'resource_path': resource_path
            }
        )
        tags_list.append(
            {
                'tag': res,
                'attr': attr,
                'new_attr_value': new_attr_value
            }
        )
    logger.info('I found {} res'.format(len(filter_resources)))
    return filter_resources, tags_list


def download_content(resources):
    logger.info("HERE IN download_content")
    count = len(resources)
    logger.info('I will download {} content links'.format(count))
    with Bar("Processing", max=count) as bar:
        for res in resources:
            print("RES in down {}".format(res))
            logger.info('Resourse {}'.format(res))
            try:
                get_web_resource(
                    res['resource_url'], res['resource_path'])
                bar.next()
            except (PermissionError, requests.RequestException) as e:
                logger.warning(e)
                logger.warning('Сan`t download {}'.format(res['resource_url']))
                pass
        bar.finish()


def update_html(page_path, soup):
    with open(page_path, 'w') as hp:
        hp.write(soup.prettify())


def compare_host_name(url, parent_url):
    url_domain = urlparse(url).netloc
    same_domain_name = urlparse(url).netloc != urlparse(parent_url).netloc
    return not (url_domain and same_domain_name)


def get_web_resource(url, path):
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1000):
            file.write(chunk)
    logger.debug('The resource was saved successfully.')


def replace_res_path(tags):
    logger.debug("Replace old page resource paths with new ones")
    for tag in tags:
        new_tag = tag['tag']
        new_tag[tag['attr']] = tag['new_attr_value']
