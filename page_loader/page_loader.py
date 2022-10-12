import os
from page_loader.page import make_page_path, get_soup, make_url_request
from page_loader.directory import create_dir, chech_dir_access
from page_loader.work_with_content import find_resources, update_html
from page_loader.work_with_content import download_content, replace_res_path
from logs.log_config import logger


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}"
    )
    checked_dir = chech_dir_access(destination_dir_name)
    page_response = make_url_request(page_url)
    soup = get_soup(page_response)
    page_path = make_page_path(page_url, checked_dir)
    dir_name, dir_path = create_dir(checked_dir, page_url)
    resourses, tags_list = find_resources(soup, dir_path, page_url)
    download_content(resourses)
    replace_res_path(tags_list)
    update_html(page_path, soup)
    logger.debug("Here is final PATH {}".format(page_path))
    return page_path
