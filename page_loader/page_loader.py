import os
from page_loader.page import download_page
from page_loader.directory import create_dir, dir_validation
from page_loader.work_with_content import download_content, save_files
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    checked_dir = dir_validation(destination_dir_name)
    page_path = download_page(page_url, checked_dir)
    dir_for_files = create_dir(checked_dir, page_url)

    content = save_files(page_path, dir_for_files, page_url)
    download_content(content, checked_dir)
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
