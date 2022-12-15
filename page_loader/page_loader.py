import os
from bs4 import BeautifulSoup
from page_loader.io import get_page_content
from page_loader.io import make_page_path, write_data_to_file
from page_loader.io import create_dir, check_dir_access
from page_loader.work_with_content import find_resources
from page_loader.work_with_content import download_content, replace_res_path
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    check_dir_access(destination_dir_name)
    page_content = get_page_content(page_url)
    soup = BeautifulSoup(page_content, "html.parser")
    page_path = make_page_path(page_url, destination_dir_name)
    dir_path = create_dir(destination_dir_name, page_url)
    resourses, tags_list = find_resources(soup, dir_path, page_url)
    download_content(resourses)
    replace_res_path(tags_list)
    write_data_to_file(page_path, soup.prettify())
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
