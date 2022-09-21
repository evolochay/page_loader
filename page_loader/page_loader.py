import os
from page_loader.page import download_page
from page_loader.directory import create_dir, chech_dir_access
from page_loader.work_with_content import download_content
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    checked_dir = chech_dir_access(destination_dir_name)
    page_path = download_page(page_url, checked_dir)
    dir_name, dir_path = create_dir(checked_dir, page_url)
    download_content(page_url, page_path, dir_path, dir_name)
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
