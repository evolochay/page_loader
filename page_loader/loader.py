import os
import shutil
from page_loader.functions import logger, create_dir
from page_loader.functions import save_files, download_page, download_content


def download(page_url, destination_dir_name):
    logger.info(f"requested url: {page_url}")
    logger.info(
        f"output path:{os.path.join(os.getcwd(), destination_dir_name)}")
    try:
        page_path = download_page(page_url, destination_dir_name)
        dir_for_files = create_dir(destination_dir_name, page_url)
        content = save_files(page_path, dir_for_files, page_url)
        download_content(content, destination_dir_name)
        logger.debug('Here is final PATH {}'.format(page_path))
        return page_path
    except Exception:
        shutil.rmtree(dir_for_files)
        raise
    except FileExistsError:
        raise
