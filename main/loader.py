import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def download(dir_name, page_adress):
    #main page download
    page_for_saving = requests.get(page_adress)
    soup = BeautifulSoup(page_for_saving.text, 'html.parser')

    #create dir for files
    resources_dir = create_name(page_adress, 'directory')
    files_dir_path = os.path.join(dir_name+'/', resources_dir)
    create_dir(files_dir_path)
    
    #download image
    domen_name = find_domen_name(page_adress)
    image_url = domen_name + find_image_path(soup)
    image_name = create_name(image_url, 'image')
    # image_url https://mikhailovsky.ru/upload/resize_cache/iblock/3f2/336_336_1/kurenkova_ekaterina.jpg
    image_link = download_image(image_url, image_name, files_dir_path)


    page_name = create_name(page_adress, 'page')
    if os.path.isdir(dir_name):
        file_full_path = os.path.join(dir_name+'/', page_name)
        with open(file_full_path, 'w') as new_file:
            new_file.write(soup.prettify())
        return file_full_path


def create_name(some_url, type):    
    without_scheme = some_url[some_url.find('//') + 2:]
    get_extension = os.path.splitext(some_url)
    if type == 'image':
        name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme[:-4]) + get_extension[1]
    elif type == 'page':
        name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme) + '.html'
    elif type == 'directory':
        name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme[:-1]) + '_files'
    return name


def find_image_path(soup):
    resource_dict = {'img': 'src'}
    images = soup.find_all(resource_dict)
    for image in images:
        return(image['src'])


def find_domen_name(url):
    full_adress = urlparse(url)
    return (full_adress.scheme+"://"+full_adress.netloc)


def download_image(image_url, image_name, dir_path):
    print('URL {}'.format(image_url))
    print('NAME {}'.format(image_name))
    print('DIR {}'.format(dir_path))

    response = requests.get(image_url)
    if response.ok:
        full_path = os.path.join(dir_path+'/', image_name)
        with open(full_path, 'wb') as f:
            f.write(response.content)
        return full_path


def create_dir(path):
   # head = os.path.split(url)[0]
    if not os.path.exists(path):
        os.mkdir(path)
