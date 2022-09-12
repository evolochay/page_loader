import re
import os
from urllib.parse import urlparse, urlunparse


def create_name(url, ext):
    url_parts = list(urlparse(url))
    url_parts[0] = ""
    without_scheme = urlunparse(url_parts)
    if without_scheme[-1] == "/":
        without_scheme = without_scheme[: len(without_scheme) - 1]
    path_part, ending = os.path.splitext(without_scheme)

    if ext == "dir":
        result = "-".join(re.findall(r"\w+", path_part + ending)) + "_files"
    elif ext == "page" or ending == "":
        result = "-".join(re.findall(r"\w+", path_part + ending)) + ".html"
    else:
        result = "-".join(re.findall(r"\w+", path_part)) + ending
    return result


def make_clear_url(url):
    parse_url = urlparse(url)
    return parse_url.scheme + "//" + parse_url.netloc
