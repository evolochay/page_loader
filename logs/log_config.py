import logging


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s :: %(name)s: %(lineno)s :: %(levelname)s :: %(message)s'
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FORMAT))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.debug('logger was initialized')

logger = logging.getLogger(__name__)
