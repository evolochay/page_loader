import requests
import re
import os


def download(dir_name, page_adress):
    text_from_url = get_page(page_adress).text
    file_name = create_file_name(page_adress)
    if os.path.isdir(dir_name):
        file_full_path = os.path.join(dir_name+'/', file_name)
        with open(file_full_path, 'w') as new_file:
            new_file.write(text_from_url)
        return file_full_path


def get_page(page_url):
    downloaded_page = requests.get(page_url)
    return downloaded_page


def create_file_name(page_adress):
    without_scheme = page_adress[page_adress.find('//') + 2:]
    file_name = re.sub(r'[^a-zA-Z0-9]', '-', without_scheme) + '.html'
    return file_name
