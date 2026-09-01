import logging
import sys

from src.config import get_settings


def setup_logging():
    settings = get_settings()
    level = (
        logging.DEBUG
        if settings.debug
        else logging.INFO
    )

    fmt = (
        "%(asctime)s [%(levelname)s] %(message)s"
        if not settings.debug
        else "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True,
    )
