"""Application-wide logging configuration."""

import logging

from rich.logging import RichHandler

from config import settings


def setup_logging() -> None:
    """Configures basic logging for the application."""
    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Rich settings
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    rich_handler = RichHandler(
        show_time=True,
        show_level=True,
        show_path=False,
        markup=True,
        tracebacks_word_wrap=True,
        tracebacks_suppress=[
            logging,
        ],
    )

    root_logger.addHandler(rich_handler)

    if len(root_logger.handlers) > 1:
        root_logger.handlers = [rich_handler]

    logging.getLogger("requests").setLevel(logging.WARNING)
