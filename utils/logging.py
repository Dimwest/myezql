import logging
from time import time
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def with_logging(func):
    def wrapper(*args, **kwargs):

        logger.info(f'Running: {func.__name__}')
        ts = time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Error during execution of {func.__name__}:\n\n{type(e)}\n{e}')
            return
        te = time()
        logger.info(f'Completed: {func.__name__}' + f' in {te-ts:.3f} sec')
        return result

    return wrapper
