from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from progress.bar import Bar
import os
from page_loader.naming import create_name
from page_loader.directory import make_path
from page_loader.page import writing, make_url_request
from logs.log_config import logger


def find_files(resource_dict, soup, domain_name, url, base_path_name):
    result_list = []
    for tag, atr in resource_dict.items():
        all_links = soup.find_all(tag, attrs={atr: True})
        for link in all_links:
            source_url = link[atr]
            source_dn = urlparse(source_url).netloc
            if source_dn == domain_name or source_dn == "":
                if source_dn == "":
                    source_url = urljoin(url, source_url)
                name = create_name(source_url, "file")
                logger.info("File name: {}".format(name))
                relative_path = make_path(base_path_name, name)
                res_description = dict(
                    [
                        ("tag", tag),
                        ("source", source_url),
                        ("rel_path", relative_path),
                    ]
                )
                result_list.append(res_description)
                link[atr] = relative_path
    return result_list


def save_files(page_path, dir_path, url):
    base_path_name = os.path.basename(dir_path)
    domain_name = urlparse(url).netloc
    resource_dict = {"img": "src", "link": "href", "script": "src"}
    result_list = []
    with open(page_path, "r", encoding="utf-8") as hp:
        soup = BeautifulSoup(hp.read(), "html.parser")
        result_list = find_files(
            resource_dict, soup, domain_name, url, base_path_name
        )
    with open(page_path, "w") as f:
        f.write(soup.prettify())
    return result_list


def download_content(resources_dict, output_path):
    count = len(resources_dict)
    with Bar("Processing", max=count) as bar:
        for res in resources_dict:
            loading_res(res, output_path)
            bar.next()


def loading_res(res_description, output_path):
    source = res_description["source"]
    rel_path = make_path(output_path, res_description["rel_path"])
    data = make_url_request(source)
    writing(rel_path, data, bytes=True)
