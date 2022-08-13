import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os
import logging

logger = logging.getLogger("app.repository")


def download_page(url, path):
    logger.info('download html page: {}'.format(url))
    html_name = create_name(url, 'page')
    new_html = make_path(path, html_name)
    content = make_url_request(url)
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
        without_scheme = without_scheme[:len(without_scheme)-1]
    path_part, ending = os.path.splitext(without_scheme)
    logger.info('Ending {}'.format(ending))

    if ext == 'dir':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '_files'
    elif ext == 'page' or ending == '':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '.html'
    else:
        result = '-'.join(re.findall(r'\w+', path_part)) + ending
    return result


def create_dir(dir_name, page_adress):
    resources_dir = create_name(page_adress, "dir")
    files_dir_path = os.path.join(dir_name+'/', resources_dir)
    print(files_dir_path)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    return files_dir_path


def save_files(page_path, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domain_name = urlparse(url).netloc
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    result_list = []
    with open(page_path, 'r', encoding='utf-8') as hp:
        soup = BeautifulSoup(hp.read(), 'html.parser')

        for tag, atr in resource_dict.items():
            all_links = soup.find_all(tag, attrs={atr: True})
            for link in all_links:
                source_url = link[atr]
                source_dn = urlparse(source_url).netloc
                if source_dn == domain_name or source_dn == '':
                    if source_dn == '':
                        source_url = urljoin(url, source_url)
                    name = create_name(source_url, 'file')
                    logger.debug('File name: {}'.format(name))
                    relative_path = make_path(base_path_name, name)
                    res_description = dict([('tag', tag),
                                            ('source', source_url),
                                            ('rel_path', relative_path)])
                    result_list.append(res_description)
                    link[atr] = relative_path
    with open(page_path, 'w') as f:
        f.write(soup.prettify())
    return result_list


def download_content(resources_dict, output_path):
    for res in resources_dict:
        loading_res(res, output_path)


def loading_res(res_description, output_path):
    tag = res_description['tag']
    source = res_description['source']
    rel_path = make_path(output_path, res_description['rel_path'])
    if tag == 'img':
        data = make_url_request(source, bytes=True)
        writing(rel_path, data, bytes=True)
    elif tag == 'link' or tag == 'script':
        data = make_url_request(source, bytes=True)
        writing(rel_path, data, bytes=True)


def make_url_request(url, bytes=False):
    logger.info('Here is URL {}'.format(url))
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("problem with server`s response {}".format(url))
            raise requests.exceptions.HTTPError
        else:
            if bytes is True:
                result = response.content
            else:
                result = response.text
            return result
    except Exception as error:  # requests.exceptions.RequestException as e:
        raise logger.error(error)
        # raise sys.exit()
