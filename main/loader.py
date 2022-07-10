import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


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
    print('МОЖЕТ БЫТЬ ЭТО {}'.format(resources_dir))
    files_dir_path = os.path.join(dir_name+'/', resources_dir)
    if not os.path.exists(files_dir_path):
        os.mkdir(files_dir_path)
    return files_dir_path


def create_soup(url):
    page_for_saving = requests.get(url)
    soup = BeautifulSoup(page_for_saving.text, 'html.parser')
    return soup


def save_files(soup, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domen = find_domen_name(url)
    print("URL {} DOMEN {}".format(url, domen))
    resource_dict = {'img': 'src'}
    all_image_links = soup.find_all(resource_dict)
    for image in all_image_links:
        source_image = image.get('src')
        name = create_name(source_image, 'image')
        local_path = os.path.join(dir_path, name)
        relative_path = ('/'+os.path.join(base_path_name, name))
        response = requests.get(domen+source_image)
        with open(local_path, 'wb') as f:
            f.write(response.content)

        for source in all_image_links:
            source['src'] = source['src'].replace(source_image, relative_path)
