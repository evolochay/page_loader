import logging
import requests
import re
import os
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse

logger = logging.getLogger("app.repository")


def download(page_adress, destination_dir_name):
    logger.info(f"requested url: {page_adress}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}")
    dir_for_files = create_dir(destination_dir_name, page_adress)
    soup = create_soup(page_adress)
    save_files(soup, dir_for_files, page_adress)
    file_full_path = create_html(soup, page_adress, destination_dir_name)

    return file_full_path


def create_html(soup, url, folder):
    html_name = create_name(url, "page")
    page_path = os.path.join(folder+'/', html_name)
    if os.path.isdir(folder):
        with open(page_path, 'w') as new_file:
            new_file.write(soup.prettify())
    return page_path


def clearing_url(url):
    url_parse = urlparse(url)
    url_netloc = url_parse.netloc
    url_path = url_parse.path
    clear_url = url_netloc + url_path
    return clear_url


def create_name(url, ext):
    url_parts = list(urlparse(url))
    url_parts[0] = ''
    without_scheme = urlunparse(url_parts)
    if without_scheme[-1] == '/':
        without_scheme = without_scheme[:len(without_scheme)-1]
    path_part, ending = os.path.splitext(without_scheme)

    if ext == 'dir':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '_files'
    elif ext == 'page':
        result = '-'.join(re.findall(r'\w+', path_part + ending)) + '.html'
    else:
        result = '-'.join(re.findall(r'\w+', path_part)) + ending
    return result


def find_domen_name(url):
    full_adress = urlparse(url)
    return (full_adress.scheme+"://"+full_adress.netloc)


def create_dir(dir_name, page_adress):
    resources_dir = create_name(page_adress, "dir")
    files_dir_path = os.path.join(dir_name+'/', resources_dir)
    print(files_dir_path)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    return files_dir_path


def create_soup(url):
    page_for_saving = make_url_request(url)
    soup = BeautifulSoup(page_for_saving.text, 'html.parser')
    return soup


def save_files(soup, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domain_name = urlparse(url).netloc
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    for teg, atr in resource_dict.items():
        all_links = soup.find_all(teg, attrs={atr: True})
        for link in all_links:
            source_url = link[atr]
            source_domain_name = urlparse(source_url).netloc
            if not source_domain_name or domain_name in source_domain_name:
                if not source_domain_name:
                    source_url = urljoin(url, source_url)

                name = create_name(source_url, 'file')
                local_path = os.path.join(dir_path, name)
                relative_path = ('/'+os.path.join(base_path_name, name))
                response = make_url_request(source_url)
                link[atr] = relative_path
                try:
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                except IOError as error:
                    logger.error("Access denied {}".format(error))


def make_url_request(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(response.status_code)
            logger.error("problem with server`s response {}".format(url))
            raise requests.exceptions.HTTPError
        else:
            return response
    except requests.exceptions.RequestException as error:
        logger.error("We`ve got {}".format(error))
        raise sys.exit()
