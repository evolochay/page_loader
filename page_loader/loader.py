import os
import shutil
from page_loader.functions import logger, create_dir, create_soup
from page_loader.functions import save_files, create_html


def download(page_adress, destination_dir_name):
    logger.info(f"requested url: {page_adress}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}")
    try:
        soup = create_soup(page_adress)
        file_full_path = create_html(soup, page_adress, destination_dir_name)
        dir_for_files = create_dir(destination_dir_name, page_adress)
        save_files(soup, dir_for_files, page_adress)
        return file_full_path
    except Exception:
        shutil.rmtree(dir_for_files)
        raise
