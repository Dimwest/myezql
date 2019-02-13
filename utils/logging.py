import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def set_verbosity(v: str):

    """
    Modifies verbosity of logger stream handler.
    :param v: verbosity level, one of: v, vv, vvv, vvvv

    :return: updated logger
    """

    if v:

        levels = {
            'v': logging.ERROR,
            'vv': logging.WARN,
            'vvv': logging.INFO,
            'vvvv': logging.DEBUG,
        }

        logger.removeHandler(handler)
        new_handler = logging.StreamHandler(sys.stdout)
        new_handler.setLevel(levels[v])
        logger.addHandler(new_handler)
        logger.warning(f"\nVerbosity level set on {levels[v]}")
