"""Utility functions."""

import logging
import sys
from datetime import UTC, datetime


class LoggingFormatter(logging.Formatter):
    """Custom formatter for logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the record to a string.

        Args:
            record: The record to format.

        Returns:
            The formatted record as a string.
        """
        timestamp = datetime.now(UTC).astimezone().isoformat()

        log_msg = (
            f"time={timestamp}"
            f" level={record.levelname}"
            f" msg='{record.getMessage()}'"
        )

        if hasattr(record, "request") and (req := record.request):
            log_msg += (
                f" ip={req.client.host}:{req.client.port}"
                f" proto={req.scope['scheme'].upper()}/{req.scope['http_version']}"
                f" method={req.method}"
                f" uri={req.url.path}"
            )

        return log_msg


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """Setup logging for the application.

    Args:
        level: The logging level to use.

    Returns:
        The root logger.
    """
    # Disable Granian's default logging
    root_logger = logging.getLogger(__name__)
    root_logger.setLevel(level)

    custom_logger = logging.getLogger("_fastagent")
    custom_logger.setLevel(level)
    custom_logger.propagate = False

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = LoggingFormatter()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    custom_logger.addHandler(console_handler)

    return root_logger
