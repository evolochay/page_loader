import re
import os
from urllib.parse import urlparse, urlunparse


def create_dir_name(page_adress):
    path_part, ending = prepare_url_to_name_creation(page_adress)
    return "-".join(re.findall(r"\w+", path_part + ending)) + "_files"


def create_page_name(url):
    path_part, ending = prepare_url_to_name_creation(url)
    return "-".join(re.findall(r"\w+", path_part + ending)) + ".html"


def create_file_name(url):
    path_part, ending = prepare_url_to_name_creation(url)
    result = "-".join(re.findall(r"\w+", path_part))
    if ending == "":
        return result + ".html"
    return result + ending


def prepare_url_to_name_creation(url):
    url_parts = list(urlparse(url))
    url_parts[0] = ""
    without_scheme = urlunparse(url_parts)
    if without_scheme[-1] == "/":
        without_scheme = without_scheme[: len(without_scheme) - 1]
    path_part, ending = os.path.splitext(without_scheme)
    return path_part, ending


def make_clear_url(url):
    parse_url = urlparse(url)
    return parse_url.scheme + "://" + parse_url.netloc


def make_url_with_scheme(page_url, res_url):
    parse_url = urlparse(res_url)
    if parse_url.scheme:
        return res_url
    else:
        return page_url + res_url
