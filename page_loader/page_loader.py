import os
import shutil
from page_loader.functions import logger, create_dir, download_content
from page_loader.functions import save_files, download_page, dir_validation


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}")
    try:
        checked_dir = dir_validation(destination_dir_name)
        page_path = download_page(page_url, checked_dir)
        dir_for_files = create_dir(checked_dir, page_url)
        content = save_files(page_path, dir_for_files, page_url)
        download_content(content, checked_dir)
        logger.debug('Here is final PATH {}'.format(page_path))
        return page_path
    except FileExistsError:
        raise
    except Exception:
        shutil.rmtree(dir_for_files)
        raise
