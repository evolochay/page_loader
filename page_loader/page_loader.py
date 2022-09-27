import os
from page_loader.page import make_page_path, get_soup
from page_loader.directory import create_dir, chech_dir_access
from page_loader.work_with_content import download_content, find_content
from page_loader.naming import make_clear_url
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    checked_dir = chech_dir_access(destination_dir_name)
    soup = get_soup(page_url)
    resourses = find_content(soup, page_url)
    page_path = make_page_path(page_url, checked_dir)
    dir_name, dir_path = create_dir(checked_dir, page_url)
    clear_url = make_clear_url(page_url)
    download_content(clear_url, page_path, dir_path, dir_name, resourses, soup)
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
