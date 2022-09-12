import os
from page_loader.page import download_page, get_soup
from page_loader.directory import create_dir, dir_validation
from page_loader.work_with_content import download_content, find_content
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    checked_dir = dir_validation(destination_dir_name)
    page_path = download_page(page_url, checked_dir)
    dir_name, dir_path = create_dir(checked_dir, page_url)
    soup = get_soup(page_path)
    content = find_content(soup, page_url)
    logger.info("PAGE URL {}".format(page_url))
    download_content(content, page_path, dir_path, dir_name, soup)
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
