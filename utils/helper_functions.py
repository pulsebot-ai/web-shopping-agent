import logging
import sys


def get_custom_logger(name: str = 'shopping_app'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s - %(name)s - %(module)s - Line %(lineno)d: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
