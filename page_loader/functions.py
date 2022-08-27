import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os
import logging
from progress.bar import Bar

logger = logging.getLogger("app.repository")


def make_url_request(url, bytes=False):
    logger.info('Here is URL {}'.format(url))
    response = requests.get(url)
    if response.status_code != 200:
        logger.warning("problem with server`s response {}".format(url))
    else:
        return check_bytes(response, bytes)


def check_bytes(response, bytes):
    if bytes is True:
        return response.content
    else:
        return response.text


def download_page(url, path, get_content=make_url_request):
    logger.info('download html page: {}'.format(url))
    html_name = create_name(url, 'page')
    new_html = make_path(path, html_name)
    content = get_content(url)
    writing(new_html, content)
    return new_html


def writing(file, data, bytes=False):
    if bytes is True:
        tag = 'wb'
    else:
        tag = 'w'
    with open(file, tag) as f:
        f.write(data)


def make_path(path, file_name):
    return os.path.join(path, file_name)


def create_name(url, ext):
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    without_scheme = urlunparse(url_parts)
    if without_scheme[-1] == '/':
        without_scheme = without_scheme[:len(without_scheme) - 1]
    path_part, ending = os.path.splitext(without_scheme)

    if ext == 'dir':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '_files'
    elif ext == 'page' or ending == '':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '.html'
    else:
        result = '-'.join(re.findall(r'\w+', path_part)) + ending
    return result


def create_dir(dir_name, page_adress):
    resources_dir = create_name(page_adress, "dir")
    files_dir_path = make_path(dir_name, resources_dir)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    return files_dir_path


def find_files(resource_dict, soup, domain_name, url, base_path_name):
    result_list = []
    for tag, atr in resource_dict.items():
        all_links = soup.find_all(tag, attrs={atr: True})
        for link in all_links:
            source_url = link[atr]
            source_dn = urlparse(source_url).netloc
            if source_dn == domain_name or source_dn == '':
                if source_dn == '':
                    source_url = urljoin(url, source_url)
                name = create_name(source_url, 'file')
                logger.info('File name: {}'.format(name))
                relative_path = make_path(base_path_name, name)
                res_description = dict([('tag', tag),
                                        ('source', source_url),
                                        ('rel_path', relative_path)])
                result_list.append(res_description)
                link[atr] = relative_path
    return result_list


def save_files(page_path, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domain_name = urlparse(url).netloc
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    result_list = []
    with open(page_path, 'r', encoding='utf-8') as hp:
        soup = BeautifulSoup(hp.read(), 'html.parser')
        result_list = find_files(resource_dict, soup, domain_name,
                                 url, base_path_name)
    with open(page_path, 'w') as f:
        f.write(soup.prettify())
    return result_list


def download_content(resources_dict, output_path):
    count = len(resources_dict)
    with Bar('Processing', max=count) as bar:
        for res in resources_dict:
            loading_res(res, output_path)
            bar.next()


def loading_res(res_description, output_path):
    source = res_description['source']
    rel_path = make_path(output_path, res_description['rel_path'])
    data = make_url_request(source, bytes=True)
    writing(rel_path, data, bytes=True)


def dir_validation(dir_path):
    if not os.access(dir_path, os.R_OK & os.W_OK & os.X_OK):
        logger.error("You may not use this directory")
    else:
        return dir_path
