import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def download(destination_dir_name, page_adress):
    dir_for_files = create_dir(destination_dir_name, page_adress)
    soup = create_soup(page_adress)
    save_files(soup, dir_for_files, page_adress)
    file_full_path = create_html(soup, page_adress, destination_dir_name)

    return file_full_path


def create_html(soup, url, folder):
    html_name = create_name(url, 'page')
    page_path = os.path.join(folder+'/', html_name)
    if os.path.isdir(folder):
        with open(page_path, 'w') as new_file:
            new_file.write(soup.prettify())
    return page_path


def create_name(some_url, type):
    without_scheme = some_url[some_url.find('//') + 2:]
    get_extension = os.path.splitext(some_url)
    if type == 'image':
        name = re.sub(r'[^a-zA-Z0-9]', '-',
                      without_scheme[:-4]) + get_extension[1]
    elif type == 'page':
        name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme) + '.html'
    elif type == 'directory':
        name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme) + '_files'
    return name


def find_domen_name(url):
    full_adress = urlparse(url)
    return (full_adress.scheme+"://"+full_adress.netloc)


def download_image(image_url, image_name, dir_path):
    response = requests.get(image_url)
    if response.ok:
        full_path = os.path.join(dir_path+'/', image_name)
        with open(full_path, 'wb') as f:
            f.write(response.content)
        return full_path


def create_dir(dir_name, page_adress):
    resources_dir = create_name(page_adress, 'directory')
    files_dir_path = os.path.join(dir_name+'/', resources_dir)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    return files_dir_path


def create_soup(url):
    print(url)
    page_for_saving = requests.get(url)
    soup = BeautifulSoup(page_for_saving.text, 'html.parser')
    return soup


def save_files(soup, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domain_name = urlparse(url).netloc
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    for teg, atr in resource_dict.items():
        all_links = soup.find_all(teg, attrs={atr: True})
        for link in all_links:
            print("LINK {}".format(link))
            source_url = link[atr]
            source_domain_name = urlparse(source_url).netloc
            print('SOURCE URL {}'.format(source_url))
            print('SOURCE domain {}'.format(source_domain_name))
            if not source_domain_name or domain_name in source_domain_name:
                if not source_domain_name:
                    source_url = urljoin(url, source_url)
                
                name = create_name(source_url, 'image')
                local_path = os.path.join(dir_path, name)
                relative_path = ('/'+os.path.join(base_path_name, name))
                print('relative_path {}'.format(relative_path))
                response = requests.get(source_url)
                link[atr] = relative_path
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                print('LINK ATTR {}'.format(link[atr]))
                
                # source_url = source_url.replace(link[atr], relative_path)
